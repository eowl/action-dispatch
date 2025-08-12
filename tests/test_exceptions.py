"""
Test cases for exception classes.
"""

import unittest

from action_dispatch.exceptions import (
    ActionDispatchError,
    HandlerNotFoundError,
    InvalidActionError,
    InvalidDimensionError,
)


class TestExceptions(unittest.TestCase):
    """Test cases for custom exception classes."""

    def test_action_dispatch_error_base(self):
        """Test ActionDispatchError base exception."""
        error = ActionDispatchError("Base error message")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Base error message")

    def test_invalid_dimension_error(self):
        """Test InvalidDimensionError exception."""
        dimension = "invalid_dim"
        available_dimensions = ["role", "environment"]

        error = InvalidDimensionError(dimension, available_dimensions)

        self.assertEqual(error.dimension, dimension)
        self.assertEqual(error.available_dimensions, available_dimensions)

        self.assertIsInstance(error, ActionDispatchError)
        self.assertIsInstance(error, Exception)

        expected_message = (
            f"Invalid dimension parameter '{dimension}', "
            f"available dimensions: {available_dimensions}"
        )
        self.assertEqual(str(error), expected_message)

    def test_handler_not_found_error(self):
        """Test HandlerNotFoundError exception."""
        action = "test_action"
        rules = {"role": "admin", "environment": "production"}

        error = HandlerNotFoundError(action, rules)

        self.assertEqual(error.action, action)
        self.assertEqual(error.rules, rules)

        self.assertIsInstance(error, ActionDispatchError)
        self.assertIsInstance(error, Exception)

        expected_message = f"No handler found for action '{action}' with rules {rules}"
        self.assertEqual(str(error), expected_message)

    def test_invalid_action_error_default(self):
        """Test InvalidActionError with default message."""
        error = InvalidActionError()

        self.assertIsInstance(error, ActionDispatchError)
        self.assertIsInstance(error, Exception)

        expected_message = "Action name must be provided for dispatching."
        self.assertEqual(str(error), expected_message)

    def test_invalid_action_error_custom_message(self):
        """Test InvalidActionError with custom message."""
        custom_message = "Custom action error message"
        error = InvalidActionError(custom_message)

        self.assertEqual(str(error), custom_message)

    def test_exception_hierarchy(self):
        """Test that all custom exceptions inherit from ActionDispatchError."""
        exceptions = [
            InvalidDimensionError("dim", ["available"]),
            HandlerNotFoundError("action", {}),
            InvalidActionError(),
        ]

        for exc in exceptions:
            self.assertIsInstance(exc, ActionDispatchError)
            self.assertIsInstance(exc, Exception)


if __name__ == "__main__":
    unittest.main()
