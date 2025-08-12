import warnings
from collections import defaultdict
from functools import partial
from typing import Any, Callable, Optional, Union

try:
    from .exceptions import (
        HandlerNotFoundError,
        InvalidActionError,
        InvalidDimensionError,
    )
except ImportError:
    pass


class ActionDispatcher:
    dimensions: list[str]
    registry: dict[str, Any]
    global_handlers: dict[str, Callable[[dict[str, Any]], Any]]

    def __init__(self, dimensions: Optional[list[str]] = None) -> None:
        if dimensions is not None and not isinstance(dimensions, list):
            warnings.warn(
                f"ActionDispatcher dimensions should be a list, got "
                f"{type(dimensions).__name__}. Setting to empty list."
            )
            self.dimensions = []
        else:
            self.dimensions = dimensions or []

        self.registry = self._create_nested_dict(len(self.dimensions))
        self.global_handlers = {}

        self._create_dynamic_methods()

    def _create_nested_dict(
        self, depth: int
    ) -> Union[dict[str, Any], defaultdict[str, Any]]:
        if depth == 0:
            return {}

        return defaultdict(partial(self._create_nested_dict, depth - 1))

    def _create_dynamic_methods(self) -> None:
        def decorator_factory(
            dimensions: list[str],
        ) -> Callable[[str], Callable[..., Callable[..., Any]]]:
            def decorator(action: str, **scope_kwargs: Any) -> Callable[
                [Callable[[dict[str, Any]], Any]],
                Callable[[dict[str, Any]], Any],
            ]:
                def wrapper(
                    func: Callable[[dict[str, Any]], Any],
                ) -> Callable[[dict[str, Any]], Any]:
                    for key in scope_kwargs:
                        if key not in dimensions:
                            raise InvalidDimensionError(key, dimensions)
                    self._register_handler(action, func, scope_kwargs)

                    return func

                return wrapper

            return decorator

        def register_factory(dimensions: list[str]) -> Callable[..., None]:
            def register(
                action: str,
                handler: Callable[[dict[str, Any]], Any],
                **scope_kwargs: Any,
            ) -> None:
                for key in scope_kwargs:
                    if key not in dimensions:
                        raise InvalidDimensionError(key, dimensions)
                self._register_handler(action, handler, scope_kwargs)

            return register

        def get_handler_factory(
            dimensions: list[str],
        ) -> Callable[..., Optional[Callable[[dict[str, Any]], Any]]]:
            def get_handler(
                action: str, **scope_kwargs: Any
            ) -> Optional[Callable[[dict[str, Any]], Any]]:
                for key in scope_kwargs:
                    if key not in dimensions:
                        raise InvalidDimensionError(key, dimensions)

                return self._find_handler(action, scope_kwargs)

            return get_handler

        self.handler = decorator_factory(self.dimensions)
        self.register = register_factory(self.dimensions)
        self.get_handler = get_handler_factory(self.dimensions)
        self.on = self.handler

    def _register_handler(
        self,
        action: str,
        handler: Callable[[dict[str, Any]], Any],
        scope_kwargs: dict[str, Any],
    ) -> None:
        current_level: Any = self.registry

        for i, dim_name in enumerate(self.dimensions):
            dim_value = scope_kwargs.get(dim_name)
            if i == len(self.dimensions) - 1:
                if dim_value not in current_level:
                    current_level[dim_value] = {}
                current_level = current_level[dim_value]
            else:
                if dim_value not in current_level:
                    current_level[dim_value] = defaultdict(dict)
                current_level = current_level[dim_value]

        current_level[action] = handler

    def _find_handler(
        self, action: str, scope_kwargs: dict[str, Any]
    ) -> Optional[Callable[[dict[str, Any]], Any]]:
        if action in self.global_handlers:
            return self.global_handlers[action]
        if not self.dimensions:
            return self.registry.get(action)

        current_level: Any = self.registry
        handler = None

        for i, dim_name in enumerate(self.dimensions):
            dim_value = scope_kwargs.get(dim_name)
            if i == len(self.dimensions) - 1:
                if dim_value in current_level and action in current_level[dim_value]:
                    handler = current_level[dim_value][action]
                elif None in current_level and action in current_level[None]:
                    handler = current_level[None][action]

                break
            if dim_value and dim_value in current_level:
                current_level = current_level[dim_value]
            elif None in current_level:
                current_level = current_level[None]
            else:
                break

        return handler

    def register_global(
        self, action: str, handler: Callable[[dict[str, Any]], Any]
    ) -> None:
        self.global_handlers[action] = handler

    def global_handler(
        self, action: str
    ) -> Callable[[Callable[[dict[str, Any]], Any]], Callable[[dict[str, Any]], Any]]:
        def decorator(
            func: Callable[[dict[str, Any]], Any],
        ) -> Callable[[dict[str, Any]], Any]:
            self.register_global(action, func)

            return func

        return decorator

    def dispatch(self, context_object: Any, action_name: str, **kwargs: Any) -> Any:
        if not action_name:
            raise InvalidActionError()

        rules = self._build_rules(context_object)
        handler = self.get_handler(action_name, **rules)

        if not handler:
            raise HandlerNotFoundError(action_name, rules)

        params = self._build_params(context_object, **kwargs)

        return handler(params)

    def _build_rules(self, context_object: Any) -> dict[str, Any]:
        rules = {}
        for dim in self.dimensions:
            if hasattr(context_object, dim):
                rules[dim] = getattr(context_object, dim)

        return rules

    def _build_params(self, context_object: Any, **kwargs: Any) -> dict[str, Any]:
        return {"context_object": context_object, **kwargs}
