"""Tests for cache functionality."""

import unittest

from action_dispatch import ActionDispatcher


class TestCacheBasic(unittest.TestCase):
    """Test basic cache functionality."""

    def test_cache_disabled_by_default(self):
        """Test that cache is disabled by default."""
        dispatcher = ActionDispatcher(dimensions=["platform"])
        self.assertFalse(dispatcher.is_cache_enabled)

    def test_enable_cache_on_init(self):
        """Test enabling cache on initialization."""
        dispatcher = ActionDispatcher(
            dimensions=["platform"],
            enable_cache=True,
            cache_maxsize=128,
        )
        self.assertTrue(dispatcher.is_cache_enabled)

    def test_enable_cache_at_runtime(self):
        """Test enabling cache at runtime."""
        dispatcher = ActionDispatcher(dimensions=["platform"])
        self.assertFalse(dispatcher.is_cache_enabled)

        dispatcher.enable_cache(maxsize=64)
        self.assertTrue(dispatcher.is_cache_enabled)

    def test_disable_cache(self):
        """Test disabling cache."""
        dispatcher = ActionDispatcher(
            dimensions=["platform"],
            enable_cache=True,
        )
        self.assertTrue(dispatcher.is_cache_enabled)

        dispatcher.disable_cache()
        self.assertFalse(dispatcher.is_cache_enabled)


class TestCacheInfo(unittest.TestCase):
    """Test cache info functionality."""

    def test_cache_info_when_disabled(self):
        """Test that cache_info returns None when cache is disabled."""
        dispatcher = ActionDispatcher(dimensions=["platform"])
        self.assertIsNone(dispatcher.cache_info())

    def test_cache_info_when_enabled(self):
        """Test that cache_info returns stats when cache is enabled."""
        dispatcher = ActionDispatcher(
            dimensions=["platform"],
            enable_cache=True,
        )

        @dispatcher.handler("test_action", platform="mobile")
        def handler(params):
            return "result"

        # Make some lookups
        dispatcher.get_handler("test_action", platform="mobile")
        dispatcher.get_handler("test_action", platform="mobile")

        info = dispatcher.cache_info()
        self.assertIsNotNone(info)
        self.assertIn("hits", info)
        self.assertIn("misses", info)
        self.assertIn("maxsize", info)
        self.assertIn("currsize", info)

    def test_cache_hits_and_misses(self):
        """Test that cache tracks hits and misses correctly."""
        dispatcher = ActionDispatcher(
            dimensions=["platform"],
            enable_cache=True,
        )

        @dispatcher.handler("test_action", platform="mobile")
        def handler(params):
            return "result"

        # First lookup - miss
        dispatcher.get_handler("test_action", platform="mobile")
        info = dispatcher.cache_info()
        self.assertEqual(info["misses"], 1)
        self.assertEqual(info["hits"], 0)

        # Second lookup - hit
        dispatcher.get_handler("test_action", platform="mobile")
        info = dispatcher.cache_info()
        self.assertEqual(info["misses"], 1)
        self.assertEqual(info["hits"], 1)


class TestCacheClear(unittest.TestCase):
    """Test cache clear functionality."""

    def test_clear_cache(self):
        """Test clearing the cache."""
        dispatcher = ActionDispatcher(
            dimensions=["platform"],
            enable_cache=True,
        )

        @dispatcher.handler("test_action", platform="mobile")
        def handler(params):
            return "result"

        # Make a lookup
        dispatcher.get_handler("test_action", platform="mobile")
        info = dispatcher.cache_info()
        self.assertEqual(info["currsize"], 1)

        # Clear cache
        dispatcher.clear_cache()
        info = dispatcher.cache_info()
        self.assertEqual(info["currsize"], 0)

    def test_cache_invalidated_on_handler_registration(self):
        """Test that cache is invalidated when new handler is registered."""
        dispatcher = ActionDispatcher(
            dimensions=["platform"],
            enable_cache=True,
        )

        @dispatcher.handler("action1", platform="mobile")
        def handler1(params):
            return "result1"

        # Make a lookup to populate cache
        dispatcher.get_handler("action1", platform="mobile")
        info = dispatcher.cache_info()
        self.assertEqual(info["currsize"], 1)

        # Register new handler - should clear cache
        @dispatcher.handler("action2", platform="desktop")
        def handler2(params):
            return "result2"

        info = dispatcher.cache_info()
        self.assertEqual(info["currsize"], 0)


class TestCacheWithDispatch(unittest.TestCase):
    """Test cache with dispatch functionality."""

    def test_dispatch_with_cache(self):
        """Test that dispatch works correctly with cache enabled."""
        dispatcher = ActionDispatcher(
            dimensions=["platform", "version"],
            enable_cache=True,
        )

        @dispatcher.handler("get_data", platform="mobile", version="2.0")
        def get_data_mobile_v2(params):
            return "data_mobile_v2"

        class Context:
            platform = "mobile"
            version = "2.0"

        result = dispatcher.dispatch(Context(), "get_data")
        self.assertEqual(result, "data_mobile_v2")

        # Second call should use cache
        result = dispatcher.dispatch(Context(), "get_data")
        self.assertEqual(result, "data_mobile_v2")

        info = dispatcher.cache_info()
        self.assertGreater(info["hits"], 0)


class TestCacheWithoutDimensions(unittest.TestCase):
    """Test cache with no dimensions."""

    def test_cache_with_no_dimensions(self):
        """Test that cache works with no dimensions."""
        dispatcher = ActionDispatcher(enable_cache=True)

        @dispatcher.handler("simple_action")
        def handler(params):
            return "simple_result"

        result = dispatcher.get_handler("simple_action")
        self.assertIsNotNone(result)

        info = dispatcher.cache_info()
        self.assertEqual(info["currsize"], 1)


if __name__ == "__main__":
    unittest.main()
