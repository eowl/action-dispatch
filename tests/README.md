# Testing Guide

This document explains how to run tests for the action-dispatch library.

## Test Structure

The tests are organized into several modules:

- `test_action_dispatcher.py` - Core functionality tests
- `test_exceptions.py` - Exception class tests
- `test_integration.py` - Integration and real-world scenario tests
- `test_config.py` - Test configuration and utilities

## Running Tests

### Run All Tests

```bash
cd /path/to/action-dispatch
python -m tests.run_tests
```

### Run Specific Test Module

```bash
# Run only core ActionDispatcher tests
python -m tests.run_tests test_action_dispatcher

# Run only exception tests
python -m tests.run_tests test_exceptions

# Run only integration tests
python -m tests.run_tests test_integration
```

### Run Individual Test Classes

```bash
python -m unittest tests.test_action_dispatcher.TestActionDispatcher
python -m unittest tests.test_exceptions.TestExceptions
```

### Run Individual Test Methods

```bash
python -m unittest tests.test_action_dispatcher.TestActionDispatcher.test_init_with_dimensions
```

## Test Coverage

The test suite includes:

### Core Functionality Tests
- Initialization with and without dimensions
- Handler registration and retrieval
- Dimension validation
- Dynamic method creation

### Handler Registration Tests
- Simple handler registration
- Multi-dimensional handler registration
- Decorator-based registration
- Invalid dimension handling

### Global Handler Tests
- Global handler registration
- Global handler priority
- Global vs scoped handler resolution

### Dispatch Tests
- Successful dispatching
- Error handling for missing handlers
- Parameter building and passing
- Context object rule extraction

### Exception Tests
- Custom exception creation
- Exception hierarchy validation
- Error message formatting

### Integration Tests
- Role-based access control simulation
- Multi-dimensional routing
- API versioning scenarios
- Permission system implementation
- Performance with large numbers of handlers

## Test Utilities

The `test_config.py` module provides:
- `BaseTestCase` - Common test functionality
- `create_mock_context()` - Helper for creating test contexts
- `suppress_warnings()` - Warning suppression for tests

## Example Test Usage

```python
import unittest
from action_dispatcher import ActionDispatcher
from exceptions import HandlerNotFoundError

class MyCustomTest(unittest.TestCase):
    def setUp(self):
        self.dispatcher = ActionDispatcher(['role', 'environment'])

    def test_my_scenario(self):
        @self.dispatcher.handler("my_action", role="admin")
        def my_handler(params):
            return "success"

        class MockContext:
            role = "admin"
            environment = "production"

        result = self.dispatcher.dispatch(MockContext(), "my_action")
        self.assertEqual(result, "success")
```

## Continuous Integration

For CI environments, run tests with:

```bash
python -m tests.run_tests
echo "Exit code: $?"
```

The test runner returns exit code 0 for success, 1 for failure.
