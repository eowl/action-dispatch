"""
Integration tests for the action-dispatch library.
"""

import unittest

from action_dispatch import ActionDispatcher
from action_dispatch.exceptions import HandlerNotFoundError


class MockUser:
    """Mock user class for testing."""

    def __init__(self, role, environment="production"):
        self.role = role
        self.environment = environment


class MockRequest:
    """Mock request class for testing."""

    def __init__(self, user, action, data=None):
        self.user = user
        self.action = action
        self.data = data or {}


class TestIntegration(unittest.TestCase):
    """Integration tests demonstrating real-world usage scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.dispatcher = ActionDispatcher(["role", "environment"])
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up test handlers for different scenarios."""

        @self.dispatcher.handler("create_user", role="admin")
        def create_user_admin(params):
            return f"Admin creating user: {params.get('username', 'unknown')}"

        @self.dispatcher.handler("create_user", role="manager")
        def create_user_manager(params):
            return f"Manager creating user: {params.get('username', 'unknown')}"

        @self.dispatcher.handler("delete_user", role="admin", environment="production")
        def delete_user_admin_prod(params):
            username = params.get("username", "unknown")
            return f"Admin deleting user in production: {username}"

        @self.dispatcher.handler("delete_user", role="admin", environment="staging")
        def delete_user_admin_staging(params):
            return (
                f"Admin deleting user in staging: {params.get('username', 'unknown')}"
            )

        @self.dispatcher.handler("view_reports", role="manager")
        def view_reports_manager(params):
            return "Manager viewing reports"

        @self.dispatcher.global_handler("health_check")
        def health_check(params):
            return "System is healthy"

    def test_role_based_dispatch(self):
        """Test dispatching based on user role."""
        admin_user = MockUser("admin")
        manager_user = MockUser("manager")

        result = self.dispatcher.dispatch(
            admin_user, "create_user", username="john_doe"
        )
        self.assertEqual(result, "Admin creating user: john_doe")

        result = self.dispatcher.dispatch(
            manager_user, "create_user", username="jane_doe"
        )
        self.assertEqual(result, "Manager creating user: jane_doe")

    def test_multi_dimensional_dispatch(self):
        """Test dispatching based on multiple dimensions."""
        admin_prod = MockUser("admin", "production")
        admin_staging = MockUser("admin", "staging")

        result = self.dispatcher.dispatch(
            admin_prod, "delete_user", username="test_user"
        )
        self.assertEqual(result, "Admin deleting user in production: test_user")

        result = self.dispatcher.dispatch(
            admin_staging, "delete_user", username="test_user"
        )
        self.assertEqual(result, "Admin deleting user in staging: test_user")

    def test_global_handler_priority(self):
        """Test that global handlers take priority."""
        user = MockUser("admin")

        result = self.dispatcher.dispatch(user, "health_check")
        self.assertEqual(result, "System is healthy")

    def test_environment_fallback(self):
        """Test environment-specific handlers."""
        env_dispatcher = ActionDispatcher(["role", "environment"])

        @env_dispatcher.handler(
            "debug_info", role="developer", environment="development"
        )
        def debug_info_dev(params):
            return "Debug info for developer in development"

        @env_dispatcher.handler("debug_info", role="admin", environment="development")
        def debug_info_admin_dev(params):
            return "Debug info for admin in development"

        dev_user = MockUser("developer", "development")
        admin_dev = MockUser("admin", "development")

        result1 = env_dispatcher.dispatch(dev_user, "debug_info")
        self.assertEqual(result1, "Debug info for developer in development")

        result2 = env_dispatcher.dispatch(admin_dev, "debug_info")
        self.assertEqual(result2, "Debug info for admin in development")

    def test_unauthorized_action(self):
        """Test handling of unauthorized actions."""
        regular_user = MockUser("user")

        with self.assertRaises(HandlerNotFoundError):
            self.dispatcher.dispatch(regular_user, "create_user", username="test")

    def test_workflow_simulation(self):
        """Test a complete workflow simulation."""
        admin = MockUser("admin", "production")
        manager = MockUser("manager", "production")

        health = self.dispatcher.dispatch(admin, "health_check")
        self.assertEqual(health, "System is healthy")

        create_result = self.dispatcher.dispatch(
            admin, "create_user", username="new_employee"
        )
        self.assertEqual(create_result, "Admin creating user: new_employee")

        delete_result = self.dispatcher.dispatch(
            admin, "delete_user", username="old_employee"
        )
        self.assertEqual(
            delete_result, "Admin deleting user in production: old_employee"
        )

        reports = self.dispatcher.dispatch(manager, "view_reports")
        self.assertEqual(reports, "Manager viewing reports")

        manager_create = self.dispatcher.dispatch(
            manager, "create_user", username="contractor"
        )
        self.assertEqual(manager_create, "Manager creating user: contractor")


class TestPerformanceAndLimits(unittest.TestCase):
    """Test performance characteristics and limits."""

    def test_large_number_of_handlers(self):
        """Test performance with large number of handlers."""
        dispatcher = ActionDispatcher(["role", "department"])

        roles = ["admin", "manager", "user", "guest"]
        departments = ["hr", "engineering", "sales", "marketing"]
        actions = ["create", "read", "update", "delete", "approve"]

        handler_count = 0
        for role in roles:
            for dept in departments:
                for action in actions:

                    def handler(params, r=role, d=dept, a=action):
                        return f"{r}_{d}_{a}"

                    dispatcher.register(action, handler, role=role, department=dept)
                    handler_count += 1

        user = MockUser("admin")
        user.department = "engineering"

        result = dispatcher.dispatch(user, "create")
        self.assertEqual(result, "admin_engineering_create")

        self.assertEqual(handler_count, len(roles) * len(departments) * len(actions))

    def test_deep_dimension_nesting(self):
        """Test with many dimensions."""
        dimensions = ["role", "department", "region", "team", "level"]
        dispatcher = ActionDispatcher(dimensions)

        def specialized_handler(params):
            return "very_specific_handler"

        dispatcher.register(
            "specialized_action",
            specialized_handler,
            role="admin",
            department="engineering",
            region="us_west",
            team="backend",
            level="senior",
        )

        context = MockUser("admin")
        context.department = "engineering"
        context.region = "us_west"
        context.team = "backend"
        context.level = "senior"

        result = dispatcher.dispatch(context, "specialized_action")
        self.assertEqual(result, "very_specific_handler")


class TestRealWorldScenarios(unittest.TestCase):
    """Test real-world usage scenarios."""

    def test_permission_system(self):
        """Test implementing a permission system."""
        dispatcher = ActionDispatcher(["role", "resource_type"])

        @dispatcher.handler("read", role="admin")
        def admin_read_all(params):
            return f"Admin reading {params.get('resource_id')}"

        @dispatcher.handler("read", role="user", resource_type="document")
        def user_read_document(params):
            return f"User reading document {params.get('resource_id')}"

        @dispatcher.handler("write", role="admin")
        def admin_write_all(params):
            return f"Admin writing to {params.get('resource_id')}"

        @dispatcher.handler("write", role="editor", resource_type="document")
        def editor_write_document(params):
            return f"Editor writing to document {params.get('resource_id')}"

        admin = MockUser("admin")
        admin.resource_type = "database"

        user = MockUser("user")
        user.resource_type = "document"

        editor = MockUser("editor")
        editor.resource_type = "document"

        result = dispatcher.dispatch(admin, "read", resource_id="secret_db")
        self.assertEqual(result, "Admin reading secret_db")

        result = dispatcher.dispatch(user, "read", resource_id="manual.pdf")
        self.assertEqual(result, "User reading document manual.pdf")

        result = dispatcher.dispatch(editor, "write", resource_id="article.md")
        self.assertEqual(result, "Editor writing to document article.md")

        with self.assertRaises(HandlerNotFoundError):
            dispatcher.dispatch(user, "write", resource_id="manual.pdf")

    def test_api_routing_simulation(self):
        """Test simulating API routing based on user context."""
        dispatcher = ActionDispatcher(["role", "api_version"])

        @dispatcher.handler("get_users", role="admin", api_version="v1")
        def get_users_admin_v1(params):
            return {"users": ["all_users"], "version": "v1", "role": "admin"}

        @dispatcher.handler("get_users", role="admin", api_version="v2")
        def get_users_admin_v2(params):
            return {
                "users": ["all_users"],
                "version": "v2",
                "role": "admin",
                "enhanced": True,
            }

        @dispatcher.handler("get_users", role="user", api_version="v2")
        def get_users_user_v2(params):
            return {
                "users": ["limited_users"],
                "version": "v2",
                "role": "user",
            }

        admin_v1 = MockUser("admin")
        admin_v1.api_version = "v1"

        admin_v2 = MockUser("admin")
        admin_v2.api_version = "v2"

        user_v2 = MockUser("user")
        user_v2.api_version = "v2"

        result1 = dispatcher.dispatch(admin_v1, "get_users")
        self.assertEqual(result1["version"], "v1")
        self.assertNotIn("enhanced", result1)

        result2 = dispatcher.dispatch(admin_v2, "get_users")
        self.assertEqual(result2["version"], "v2")
        self.assertTrue(result2["enhanced"])

        result3 = dispatcher.dispatch(user_v2, "get_users")
        self.assertEqual(result3["users"], ["limited_users"])


if __name__ == "__main__":
    unittest.main()
