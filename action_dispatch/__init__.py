"""Action Dispatch - Multi-dimensional routing system.

A Python library providing dynamic action dispatching based on context
dimensions like user roles, environments, API versions, and custom attributes.

Key Features:
- Multi-dimensional routing
- Dynamic handler registration
- Decorator-based handler definition
- Global and scoped handlers
- Type-safe custom exceptions
- Flexible context-based dispatching

Example:
    >>> from action_dispatch import ActionDispatcher
    >>> dispatcher = ActionDispatcher(['role', 'environment'])
    >>>
    >>> @dispatcher.handler("create_user", role="admin")
    >>> def admin_create_user(params):
    ...     return f"Admin creating user: {params.get('username')}"
    >>>
    >>> class Context:
    ...     def __init__(self, role, environment):
    ...         self.role = role
    ...         self.environment = environment
    >>>
    >>> context = Context("admin", "production")
    >>> result = dispatcher.dispatch(context, "create_user", username="john")
    >>> print(result)  # "Admin creating user: john"
"""

from .action_dispatcher import ActionDispatcher
from .exceptions import (
    ActionDispatchError,
    HandlerNotFoundError,
    InvalidActionError,
    InvalidDimensionError,
)
from .mixins import CacheMixin

__version__ = "0.1.1"
__author__ = "Eowl"
__email__ = "eowl@me.com"

__all__ = [
    "ActionDispatcher",
    "CacheMixin",
    "ActionDispatchError",
    "InvalidDimensionError",
    "HandlerNotFoundError",
    "InvalidActionError",
]
