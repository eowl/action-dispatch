# Contributing to Action Dispatch

Thank you for your interest in contributing to Action Dispatch! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include Python version, library version, and operating system**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the enhancement**
- **Describe the current behavior and explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, logical commits
3. **Add tests** for your changes
4. **Ensure all tests pass**
5. **Update documentation** if needed
6. **Follow the coding standards**
7. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Setup Instructions

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/action-dispatch.git
cd action-dispatch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Development Workflow

1. **Create a new branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Run tests** to ensure everything works:
   ```bash
   python -m unittest discover tests -v
   ```

4. **Run code quality checks**:
   ```bash
   black action_dispatch tests
   flake8 action_dispatch tests
   mypy action_dispatch
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** from your fork to the main repository

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Code Quality Tools

We use several tools to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Coverage**: Test coverage reporting
- **unittest**: Testing framework
- **pre-commit**: Git hooks

### Testing Guidelines

- Write tests for all new functionality
- Maintain or improve test coverage
- Use descriptive test names
- Include both positive and negative test cases
- Test edge cases and error conditions

#### Test Structure

```python
def test_feature_description(self):
    """Test that the feature works as expected."""
    # Arrange
    setup_test_data()

    # Act
    result = perform_action()

    # Assert
    self.assertEqual(result, expected_value)
```

### Documentation

- Update docstrings for any changed functions or classes
- Update README.md if adding new features
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format
- Include code examples for new features

## Commit Message Guidelines

Use clear and meaningful commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Examples:
```
Add support for custom fallback handlers

- Implement fallback mechanism for partial dimension matches
- Add tests for fallback behavior
- Update documentation with examples

Fixes #123
```

## Release Process

Releases are handled by maintainers:

1. Update version in `action_dispatch/__init__.py`
2. Update CHANGELOG.md with release notes
3. Create a git tag for the version
4. Build and upload to PyPI
5. Create GitHub release with release notes

## Questions?

If you have questions about contributing, please:

1. Check the existing issues and discussions
2. Create a new discussion on GitHub
3. Reach out to the maintainers

Thank you for contributing to Action Dispatch!
