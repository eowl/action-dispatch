# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-20

### Added
- Initial release of action-dispatch library
- Multi-dimensional action dispatching system
- Dynamic handler registration with decorators
- Global and scoped handler support
- Custom exception classes for better error handling
- Comprehensive test suite with 100% coverage
- Type hints and mypy support
- Detailed documentation and examples

### Features
- `ActionDispatcher` class for managing action routing
- `@handler` decorator for registering scoped handlers
- `@global_handler` decorator for registering global handlers
- `dispatch()` method for executing actions based on context
- Support for any number of custom dimensions
- Fallback mechanisms for partial matches
- Performance optimized for large numbers of handlers

### Exceptions
- `ActionDispatchError` - Base exception class
- `InvalidDimensionError` - Invalid dimension parameters
- `HandlerNotFoundError` - No matching handler found
- `InvalidActionError` - Invalid action name provided

### Documentation
- Complete README with examples and API reference
- Comprehensive test suite demonstrating usage patterns
- Real-world examples for web APIs, microservices, and plugins
- Development setup and contribution guidelines

[Unreleased]: https://github.com/eowl/action-dispatch/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/eowl/action-dispatch/releases/tag/v1.0.0
