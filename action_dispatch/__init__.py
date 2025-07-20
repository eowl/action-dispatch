"""
Action Dispatch - A flexible action dispatching system with multi-dimensional routing capabilities.

A powerful Python library that provides dynamic action dispatching based on context dimensions
such as user roles, environments, API versions, and any custom attributes.

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
    InvalidDimensionError,
    HandlerNotFoundError,
    InvalidActionError,
)

__version__ = "0.1.0"
__author__ = "Eowl"
__email__ = "eowl@me.com"

__all__ = [
    "ActionDispatcher",
    "ActionDispatchError",
    "InvalidDimensionError",
    "HandlerNotFoundError",
    "InvalidActionError",
]
