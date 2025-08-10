#!/usr/bin/env python3
"""
Build script for action-dispatch package.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Run a shell command and print status."""
    print(f"🔧 {description}...")
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False


def main() -> None:
    """Main build process."""
    print("🚀 Building action-dispatch package...\n")

    # Change to project root
    project_root = Path(__file__).parent
    subprocess.run(f"cd {project_root}", shell=True)

    steps = [
        ("uv run python -m unittest discover tests", "Running tests"),
        ("uv run black action_dispatch tests", "Formatting code"),
        ("uv run python -m build", "Building package"),
    ]

    all_passed = True
    for cmd, description in steps:
        if not run_command(cmd, description):
            all_passed = False
            break
        print()

    if all_passed:
        print("🎉 Package build completed successfully!")
        print("\n📦 Build artifacts:")
        print("   - dist/action_dispatch-*.whl")
        print("   - dist/action_dispatch-*.tar.gz")
        print("\n🚀 To publish to PyPI:")
        print("   - Test: uv run twine upload --repository testpypi dist/*")
        print("   - Prod: uv run twine upload dist/*")
    else:
        print("💥 Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
