"""
Action Dispatch Library

A flexible action dispatching system with multi-dimensional routing capabilities.
"""

from .action_dispatcher import ActionDispatcher
from .exceptions import (
    ActionDispatchError,
    InvalidDimensionError,
    HandlerNotFoundError,
    InvalidActionError
)

__version__ = "1.0.0"
__all__ = [
    "ActionDispatcher",
    "ActionDispatchError",
    "InvalidDimensionError",
    "HandlerNotFoundError", 
    "InvalidActionError"
]
