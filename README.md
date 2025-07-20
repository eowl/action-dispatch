# Action Dispatch

[![PyPI version](https://badge.fury.io/py/action-dispatch.svg)](https://badge.fury.io/py/action-dispatch)
[![Python Support](https://img.shields.io/pypi/pyversions/action-dispatch.svg)](https://pypi.org/project/action-dispatch/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/eowl/action-dispatch/workflows/Tests/badge.svg)](https://github.com/eowl/action-dispatch/actions)

A powerful and flexible Python library for multi-dimensional action dispatching. Route function calls dynamically based on context dimensions like user roles, environments, API versions, or any custom attributes.

## Features

🚀 **Multi-dimensional Routing** - Dispatch based on multiple context attributes simultaneously  
🎯 **Dynamic Handler Registration** - Register handlers using decorators or programmatically  
🔧 **Flexible Context Matching** - Support for exact matches and fallback strategies  
⚡ **High Performance** - Efficient handler lookup even with thousands of registered handlers  
🛡️ **Type Safe** - Custom exception classes for better error handling  
📝 **Well Documented** - Comprehensive documentation and examples  
🧪 **Fully Tested** - 100% test coverage with extensive test suite  

## Installation

```bash
pip install action-dispatch
```

## Quick Start

```python
from action_dispatch import ActionDispatcher

# Create dispatcher with dimensions
dispatcher = ActionDispatcher(['role', 'environment'])

# Register handlers using decorators
@dispatcher.handler("create_user", role="admin")
def admin_create_user(params):
    return f"Admin creating user: {params.get('username')}"

@dispatcher.handler("create_user", role="manager")  
def manager_create_user(params):
    return f"Manager creating user: {params.get('username')}"

# Define context class
class RequestContext:
    def __init__(self, role, environment):
        self.role = role
        self.environment = environment

# Dispatch actions based on context
admin_context = RequestContext("admin", "production")
result = dispatcher.dispatch(admin_context, "create_user", username="john")
print(result)  # "Admin creating user: john"
```

## Advanced Usage

### Multi-dimensional Routing

```python
dispatcher = ActionDispatcher(['role', 'environment', 'feature_flag'])

@dispatcher.handler("process_payment", 
                   role="admin", 
                   environment="production", 
                   feature_flag="new_payment_system")
def new_payment_handler(params):
    return "Processing with new payment system"

@dispatcher.handler("process_payment", 
                   role="admin", 
                   environment="production")
def default_payment_handler(params):
    return "Processing with default system"
```

### Global Handlers

```python
# Global handlers work across all contexts
@dispatcher.global_handler("health_check")
def health_check(params):
    return {"status": "healthy", "timestamp": time.time()}

# Global handlers have priority over scoped handlers
result = dispatcher.dispatch(any_context, "health_check")
```

### Programmatic Registration

```python
def custom_handler(params):
    return "Custom response"

# Register without decorators
dispatcher.register("custom_action", custom_handler, role="user")

# Register global handler
dispatcher.register_global("system_status", lambda p: "OK")
```

### Error Handling

```python
from action_dispatch import HandlerNotFoundError, InvalidDimensionError

try:
    result = dispatcher.dispatch(context, "unknown_action")
except HandlerNotFoundError as e:
    print(f"No handler found for action: {e.action}")
    print(f"Context rules: {e.rules}")

try:
    dispatcher.register("action", handler, invalid_dimension="value")
except InvalidDimensionError as e:
    print(f"Invalid dimension: {e.dimension}")
    print(f"Available dimensions: {e.available_dimensions}")
```

## Real-World Examples

### Web API with Role-Based Access Control

```python
from action_dispatch import ActionDispatcher

# Set up dispatcher for API routing
api_dispatcher = ActionDispatcher(['role', 'api_version'])

@api_dispatcher.handler("get_users", role="admin", api_version="v2")
def get_users_admin_v2(params):
    return {
        "users": get_all_users(),
        "total": count_all_users(),
        "permissions": ["read", "write", "delete"]
    }

@api_dispatcher.handler("get_users", role="user", api_version="v2") 
def get_users_regular_v2(params):
    return {
        "users": get_user_own_data(params['context_object']),
        "permissions": ["read"]
    }

# API endpoint
def api_get_users(request):
    try:
        result = api_dispatcher.dispatch(
            request.user, 
            "get_users",
            request_id=request.id
        )
        return JsonResponse(result)
    except HandlerNotFoundError:
        return JsonResponse({"error": "Forbidden"}, status=403)
```

### Microservices Environment Routing

```python
service_dispatcher = ActionDispatcher(['environment', 'service_version'])

@service_dispatcher.handler("process_order", 
                           environment="production", 
                           service_version="v2")
def process_order_prod_v2(params):
    # Use production database and new algorithm
    return production_order_processor.process(params['order_data'])

@service_dispatcher.handler("process_order", 
                           environment="staging")
def process_order_staging(params):
    # Use staging database with verbose logging
    return staging_order_processor.process(params['order_data'])
```

### Plugin System

```python
plugin_dispatcher = ActionDispatcher(['plugin_type', 'version'])

# Plugins can register their handlers
@plugin_dispatcher.handler("transform_data", 
                          plugin_type="image_processor", 
                          version="2.0")
def image_transform_v2(params):
    return enhanced_image_transform(params['data'])

# Dynamic plugin loading
for plugin in load_plugins():
    plugin.register_handlers(plugin_dispatcher)

# Process with appropriate plugin
result = plugin_dispatcher.dispatch(context, "transform_data", data=input_data)
```

## API Reference

### ActionDispatcher

#### `__init__(dimensions=None)`
Create a new dispatcher with optional dimensions.

- `dimensions` (list, optional): List of dimension names for routing

#### `@handler(action, **kwargs)`
Decorator to register a handler for specific action and dimensions.

- `action` (str): Action name
- `**kwargs`: Dimension values for routing

#### `@global_handler(action)`
Decorator to register a global handler that works across all contexts.

- `action` (str): Action name

#### `register(action, handler, **kwargs)`
Programmatically register a handler.

- `action` (str): Action name  
- `handler` (callable): Handler function
- `**kwargs`: Dimension values for routing

#### `dispatch(context_object, action_name, **kwargs)`
Dispatch an action based on context.

- `context_object`: Object with dimension attributes
- `action_name` (str): Action to dispatch
- `**kwargs`: Additional parameters passed to handler

### Exceptions

- `ActionDispatchError`: Base exception class
- `InvalidDimensionError`: Raised for invalid dimension parameters
- `HandlerNotFoundError`: Raised when no handler is found
- `InvalidActionError`: Raised for invalid action names

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/eowl/action-dispatch.git
cd action-dispatch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests -v

# Run with coverage
coverage run -m unittest discover tests
coverage report
coverage html

# Run specific test file
python -m unittest tests.test_action_dispatcher -v

# Run specific test class
python -m unittest tests.test_action_dispatcher.TestActionDispatcher -v
```

### Code Quality

```bash
# Format code
black action_dispatch tests

# Lint code  
flake8 action_dispatch tests

# Type checking
mypy action_dispatch
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass (`python -m pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and releases.

## Support

- 📖 [Documentation](https://action-dispatch.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/eowl/action-dispatch/issues)
- 💬 [Discussions](https://github.com/eowl/action-dispatch/discussions)

## Acknowledgments

- Inspired by the need for flexible routing in complex applications
- Built with modern Python best practices
- Thoroughly tested and documented
