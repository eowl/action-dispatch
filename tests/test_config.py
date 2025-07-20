"""
Test configuration and utilities.
"""

import unittest
import warnings
from unittest.mock import Mock


def suppress_warnings():
    """Suppress warnings during testing."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)


def create_mock_context(role="user", **kwargs):
    """Create a mock context object with specified attributes."""
    context = Mock()
    context.role = role

    for key, value in kwargs.items():
        setattr(context, key, value)

    return context


class BaseTestCase(unittest.TestCase):
    """Base test case with common functionality."""

    def setUp(self):
        """Set up common test fixtures."""
        suppress_warnings()

    def assertRaisesWithMessage(
        self, exception_class, message_substring, callable_obj, *args, **kwargs
    ):
        """Assert that an exception is raised with a specific message."""
        with self.assertRaises(exception_class) as cm:
            callable_obj(*args, **kwargs)

        self.assertIn(message_substring, str(cm.exception))
        return cm.exception
