"""Cache mixin for ActionDispatcher."""

from functools import lru_cache
from typing import Any, Callable, Optional

# Default maximum size for LRU cache
DEFAULT_CACHE_MAXSIZE = 256


class CacheMixin:
    """
    Mixin class that adds LRU cache support to ActionDispatcher.

    This mixin provides optional caching for handler lookups,
    which can improve performance when:
    - You have many dimensions (10+)
    - You have high-frequency repeated lookups
    - The same action + scope combinations are called frequently

    Usage:
        dispatcher = ActionDispatcher(
            dimensions=["region", "platform", "version"],
            enable_cache=True,
            cache_maxsize=512  # or use default: DEFAULT_CACHE_MAXSIZE
        )
    """

    _cache_enabled: bool
    _cache_maxsize: int
    _cached_find_handler: Any  # lru_cache wrapped function

    def _init_cache(
        self,
        enable_cache: bool = False,
        cache_maxsize: int = DEFAULT_CACHE_MAXSIZE,
    ) -> None:
        """Initialize cache configuration."""
        self._cache_enabled = False
        self._cache_maxsize = cache_maxsize
        self._cached_find_handler = None

        if enable_cache:
            self._setup_cache()
            self._cache_enabled = True

    def _setup_cache(self) -> None:
        """Setup LRU cache for handler lookup."""

        @lru_cache(maxsize=self._cache_maxsize)
        def cached_find(
            action: str, scope_tuple: tuple[tuple[str, Any], ...]
        ) -> Optional[Callable[[dict[str, Any]], Any]]:
            scope_kwargs = dict(scope_tuple)
            return self._match_handler(action, scope_kwargs)

        self._cached_find_handler = cached_find

    def _find_handler_with_cache(
        self, action: str, scope_kwargs: dict[str, Any]
    ) -> Optional[Callable[[dict[str, Any]], Any]]:
        """Find handler with optional caching."""
        if self._cache_enabled and self._cached_find_handler is not None:
            scope_tuple = tuple(sorted(scope_kwargs.items()))
            result: Optional[Callable[[dict[str, Any]], Any]] = (
                self._cached_find_handler(action, scope_tuple)
            )
            return result

        return self._match_handler(action, scope_kwargs)

    def _match_handler(
        self, action: str, scope_kwargs: dict[str, Any]
    ) -> Optional[Callable[[dict[str, Any]], Any]]:
        """
        Match handler based on action and scope dimensions.

        This method should be overridden by the main class.
        """
        raise NotImplementedError("Subclass must implement _match_handler")

    def _invalidate_cache(self) -> None:
        """Invalidate cache when handlers change."""
        if self._cache_enabled:
            self.clear_cache()

    def enable_cache(self, maxsize: Optional[int] = None) -> None:
        """
        Enable LRU cache for handler lookup.

        Args:
            maxsize: Maximum cache size (uses existing value if None).
        """
        if maxsize is not None:
            self._cache_maxsize = maxsize
        self._setup_cache()
        self._cache_enabled = True

    def disable_cache(self) -> None:
        """Disable cache and clear cached data."""
        self._cache_enabled = False
        self._cached_find_handler = None

    def clear_cache(self) -> None:
        """Clear all cached handler lookups."""
        if self._cached_find_handler is not None:
            self._cached_find_handler.cache_clear()

    def cache_info(self) -> Optional[dict[str, int]]:
        """
        Get cache statistics.

        Returns:
            Dict with hits, misses, maxsize, currsize, or None if disabled.
        """
        if not self._cache_enabled or self._cached_find_handler is None:
            return None

        info = self._cached_find_handler.cache_info()
        return {
            "hits": info.hits,
            "misses": info.misses,
            "maxsize": info.maxsize or 0,
            "currsize": info.currsize,
        }

    @property
    def is_cache_enabled(self) -> bool:
        """Check if cache is currently enabled."""
        return self._cache_enabled
