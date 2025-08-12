"""
Test cases for ActionDispatcher class.
"""

import unittest
import warnings
from unittest.mock import Mock

from action_dispatch import ActionDispatcher
from action_dispatch.exceptions import (
    HandlerNotFoundError,
    InvalidActionError,
    InvalidDimensionError,
)


class TestActionDispatcher(unittest.TestCase):
    """Test cases for ActionDispatcher initialization and basic functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.dispatcher = ActionDispatcher()
        self.multi_dim_dispatcher = ActionDispatcher(["role", "environment"])

    def test_init_without_dimensions(self):
        """Test initialization without dimensions."""
        dispatcher = ActionDispatcher()
        self.assertEqual(dispatcher.dimensions, [])
        self.assertEqual(dispatcher.registry, {})
        self.assertEqual(dispatcher.global_handlers, {})

    def test_init_with_dimensions(self):
        """Test initialization with dimensions."""
        dimensions = ["role", "environment"]
        dispatcher = ActionDispatcher(dimensions)
        self.assertEqual(dispatcher.dimensions, dimensions)
        self.assertIsInstance(dispatcher.registry, dict)

    def test_init_with_invalid_dimensions_type(self):
        """Test initialization with invalid dimensions type."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            dispatcher = ActionDispatcher("invalid")
            self.assertEqual(len(w), 1)
            self.assertIn("should be a list", str(w[0].message))
            self.assertEqual(dispatcher.dimensions, [])

    def test_dynamic_methods_creation(self):
        """Test that dynamic methods are created properly."""
        self.assertTrue(hasattr(self.dispatcher, "handler"))
        self.assertTrue(hasattr(self.dispatcher, "register"))
        self.assertTrue(hasattr(self.dispatcher, "get_handler"))
        self.assertTrue(hasattr(self.dispatcher, "on"))
        self.assertEqual(self.dispatcher.on, self.dispatcher.handler)


class TestHandlerRegistration(unittest.TestCase):
    """Test cases for handler registration functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.dispatcher = ActionDispatcher()
        self.multi_dim_dispatcher = ActionDispatcher(["role", "environment"])

    def test_register_simple_handler(self):
        """Test registering a simple handler without dimensions."""

        def test_handler(params):
            return "test_result"

        self.dispatcher.register("test_action", test_handler)
        retrieved_handler = self.dispatcher.get_handler("test_action")
        self.assertEqual(retrieved_handler, test_handler)

    def test_register_handler_with_dimensions(self):
        """Test registering handler with dimensions."""

        def test_handler(params):
            return "test_result"

        self.multi_dim_dispatcher.register(
            "test_action", test_handler, role="admin", environment="production"
        )

        retrieved_handler = self.multi_dim_dispatcher.get_handler(
            "test_action", role="admin", environment="production"
        )
        self.assertEqual(retrieved_handler, test_handler)

    def test_register_handler_with_invalid_dimension(self):
        """Test registering handler with invalid dimension."""

        def test_handler(params):
            return "test_result"

        with self.assertRaises(InvalidDimensionError) as cm:
            self.multi_dim_dispatcher.register(
                "test_action", test_handler, invalid_dim="value"
            )

        self.assertEqual(cm.exception.dimension, "invalid_dim")
        self.assertEqual(cm.exception.available_dimensions, ["role", "environment"])

    def test_decorator_registration(self):
        """Test handler registration using decorator."""

        @self.dispatcher.handler("test_action")
        def test_handler(params):
            return "decorated_result"

        retrieved_handler = self.dispatcher.get_handler("test_action")
        self.assertEqual(retrieved_handler, test_handler)

    def test_decorator_registration_with_dimensions(self):
        """Test handler registration using decorator with dimensions."""

        @self.multi_dim_dispatcher.handler("test_action", role="user")
        def test_handler(params):
            return "decorated_result"

        retrieved_handler = self.multi_dim_dispatcher.get_handler(
            "test_action", role="user"
        )
        self.assertEqual(retrieved_handler, test_handler)

    def test_on_alias_decorator(self):
        """Test that 'on' is an alias for 'handler'."""

        @self.dispatcher.on("test_action")
        def test_handler(params):
            return "on_result"

        retrieved_handler = self.dispatcher.get_handler("test_action")
        self.assertEqual(retrieved_handler, test_handler)


class TestGlobalHandlers(unittest.TestCase):
    """Test cases for global handler functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.dispatcher = ActionDispatcher(["role"])

    def test_register_global_handler(self):
        """Test registering a global handler."""

        def global_handler(params):
            return "global_result"

        self.dispatcher.register_global("global_action", global_handler)
        self.assertEqual(
            self.dispatcher.global_handlers["global_action"], global_handler
        )

    def test_global_handler_decorator(self):
        """Test global handler registration using decorator."""

        @self.dispatcher.global_handler("global_action")
        def global_handler(params):
            return "global_result"

        self.assertEqual(
            self.dispatcher.global_handlers["global_action"], global_handler
        )

    def test_global_handler_priority(self):
        """Test that global handlers have priority over scoped handlers."""

        def scoped_handler(params):
            return "scoped_result"

        def global_handler(params):
            return "global_result"

        # Register scoped handler first
        self.dispatcher.register("test_action", scoped_handler, role="user")

        # Register global handler
        self.dispatcher.register_global("test_action", global_handler)

        # Global handler should be returned
        retrieved_handler = self.dispatcher.get_handler("test_action", role="user")
        self.assertEqual(retrieved_handler, global_handler)


class TestHandlerRetrieval(unittest.TestCase):
    """Test cases for handler retrieval functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.dispatcher = ActionDispatcher(["role", "environment"])

    def test_get_handler_exact_match(self):
        """Test getting handler with exact dimension match."""

        def test_handler(params):
            return "exact_match"

        self.dispatcher.register(
            "test_action", test_handler, role="admin", environment="production"
        )

        retrieved_handler = self.dispatcher.get_handler(
            "test_action", role="admin", environment="production"
        )
        self.assertEqual(retrieved_handler, test_handler)

    def test_get_handler_fallback_to_none(self):
        """Test getting handler with fallback to None dimension."""

        def fallback_handler(params):
            return "fallback_result"

        # Register handler with None for environment
        self.dispatcher.register(
            "test_action", fallback_handler, role="admin", environment=None
        )

        # Should find the handler even with different environment
        retrieved_handler = self.dispatcher.get_handler(
            "test_action", role="admin", environment="staging"
        )
        self.assertEqual(retrieved_handler, fallback_handler)

    def test_get_handler_not_found(self):
        """Test getting handler when no match is found."""
        retrieved_handler = self.dispatcher.get_handler(
            "nonexistent_action", role="admin"
        )
        self.assertIsNone(retrieved_handler)

    def test_get_handler_invalid_dimension(self):
        """Test getting handler with invalid dimension."""
        with self.assertRaises(InvalidDimensionError):
            self.dispatcher.get_handler("test_action", invalid_dim="value")


class TestDispatch(unittest.TestCase):
    """Test cases for dispatch functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.dispatcher = ActionDispatcher(["role"])

        # Create mock context object
        self.context = Mock()
        self.context.role = "admin"

    def test_successful_dispatch(self):
        """Test successful action dispatch."""

        def test_handler(params):
            return f"Hello {params['context_object'].role}"

        self.dispatcher.register("greet", test_handler, role="admin")

        result = self.dispatcher.dispatch(self.context, "greet")
        self.assertEqual(result, "Hello admin")

    def test_dispatch_with_kwargs(self):
        """Test dispatch with additional keyword arguments."""

        def test_handler(params):
            return f"Hello {params['name']} from {params['context_object'].role}"

        self.dispatcher.register("greet", test_handler, role="admin")

        result = self.dispatcher.dispatch(self.context, "greet", name="John")
        self.assertEqual(result, "Hello John from admin")

    def test_dispatch_invalid_action(self):
        """Test dispatch with invalid action name."""
        with self.assertRaises(InvalidActionError):
            self.dispatcher.dispatch(self.context, "")

        with self.assertRaises(InvalidActionError):
            self.dispatcher.dispatch(self.context, None)

    def test_dispatch_handler_not_found(self):
        """Test dispatch when no handler is found."""
        with self.assertRaises(HandlerNotFoundError) as cm:
            self.dispatcher.dispatch(self.context, "nonexistent_action")

        self.assertEqual(cm.exception.action, "nonexistent_action")
        self.assertEqual(cm.exception.rules, {"role": "admin"})

    def test_build_rules_from_context(self):
        """Test building rules from context object."""
        context = Mock()
        context.role = "user"
        context.environment = "dev"
        context.other_attr = "ignored"

        dispatcher = ActionDispatcher(["role", "environment"])
        rules = dispatcher._build_rules(context)

        expected_rules = {"role": "user", "environment": "dev"}
        self.assertEqual(rules, expected_rules)

    def test_build_rules_missing_attributes(self):
        """Test building rules when context is missing some attributes."""

        class SimpleContext:
            def __init__(self):
                self.role = "user"
                # Note: no environment attribute

        context = SimpleContext()
        dispatcher = ActionDispatcher(["role", "environment"])
        rules = dispatcher._build_rules(context)

        expected_rules = {"role": "user"}
        self.assertEqual(rules, expected_rules)

    def test_build_params(self):
        """Test building parameters for handler."""
        context = Mock()
        params = self.dispatcher._build_params(context, extra_param="value")

        expected_params = {"context_object": context, "extra_param": "value"}
        self.assertEqual(params, expected_params)


class TestNestedDictCreation(unittest.TestCase):
    """Test cases for nested dictionary creation."""

    def test_create_nested_dict_depth_zero(self):
        """Test creating nested dict with depth 0."""
        dispatcher = ActionDispatcher()
        result = dispatcher._create_nested_dict(0)
        self.assertEqual(result, {})

    def test_create_nested_dict_depth_one(self):
        """Test creating nested dict with depth 1."""
        dispatcher = ActionDispatcher()
        result = dispatcher._create_nested_dict(1)
        self.assertIsInstance(result, dict)

        # Test that it creates empty dict for new keys
        nested = result["test_key"]
        self.assertEqual(nested, {})

    def test_create_nested_dict_depth_two(self):
        """Test creating nested dict with depth 2."""
        dispatcher = ActionDispatcher()
        result = dispatcher._create_nested_dict(2)

        # Test accessing nested levels
        level1 = result["key1"]
        level2 = level1["key2"]
        self.assertEqual(level2, {})


class TestEdgeCases(unittest.TestCase):
    """Test cases for edge cases and error conditions."""

    def test_empty_dimensions_list(self):
        """Test with empty dimensions list."""
        dispatcher = ActionDispatcher([])

        def test_handler(params):
            return "result"

        dispatcher.register("test_action", test_handler)
        retrieved_handler = dispatcher.get_handler("test_action")
        self.assertEqual(retrieved_handler, test_handler)

    def test_handler_overwrite(self):
        """Test overwriting existing handler."""

        def original_handler(params):
            return "original"

        def new_handler(params):
            return "new"

        self.dispatcher = ActionDispatcher(["role"])

        # Register original handler
        self.dispatcher.register("test_action", original_handler, role="admin")

        # Overwrite with new handler
        self.dispatcher.register("test_action", new_handler, role="admin")

        retrieved_handler = self.dispatcher.get_handler("test_action", role="admin")
        self.assertEqual(retrieved_handler, new_handler)

    def test_multiple_dimensions_registration(self):
        """Test registration with multiple dimensions."""
        dispatcher = ActionDispatcher(["role", "environment", "feature"])

        def test_handler(params):
            return "complex_result"

        dispatcher.register(
            "complex_action",
            test_handler,
            role="admin",
            environment="production",
            feature="reporting",
        )

        retrieved_handler = dispatcher.get_handler(
            "complex_action",
            role="admin",
            environment="production",
            feature="reporting",
        )
        self.assertEqual(retrieved_handler, test_handler)


if __name__ == "__main__":
    unittest.main()
