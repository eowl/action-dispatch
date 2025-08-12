#!/usr/bin/env python3
"""
Test runner script for action-dispatch library.
"""

import os
import sys
import unittest

# Add the parent directory to sys.path so we can import the library
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_all_tests():
    """Run all tests in the tests directory."""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_specific_test(test_module):
    """Run a specific test module."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_module)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test module
        test_module = sys.argv[1]
        print(f"Running tests from {test_module}...")
        success = run_specific_test(test_module)
    else:
        # Run all tests
        print("Running all tests...")
        success = run_all_tests()

    sys.exit(0 if success else 1)
