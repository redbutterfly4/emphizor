#!/usr/bin/env python3
"""
Test runner for Emphizor integration tests.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*50)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def check_requirements():
    """Check if test requirements are installed"""
    print("Checking test requirements...")
    
    try:
        import pytest
        import dotenv
        print("✓ Test requirements are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing test requirements: {e}")
        print("Please install test requirements: pip install -r test_requirements.txt")
        return False

def check_test_env():
    """Check if test environment file exists"""
    if os.path.exists('test.env'):
        print("✓ test.env file found")
        return True
    else:
        print("✗ test.env file not found")
        print("Please create test.env file with test credentials")
        return False

def run_integration_tests(test_type="all", verbose=False, coverage=False):
    """Run integration tests"""
    
    # Base pytest command
    cmd = "pytest"
    
    # Add test directory
    cmd += " tests/"
    
    # Add test type filter
    if test_type != "all":
        cmd += f" -m {test_type}"
    
    # Add verbose flag
    if verbose:
        cmd += " -v"
    
    # Add coverage
    if coverage:
        cmd += " --cov=. --cov-report=html --cov-report=term-missing"
    
    # Add other useful flags
    cmd += " --tb=short"
    
    return run_command(cmd, f"Integration tests ({test_type})")

def run_specific_test(test_file, test_function=None):
    """Run a specific test file or function"""
    cmd = f"pytest tests/{test_file}"
    
    if test_function:
        cmd += f"::{test_function}"
    
    cmd += " -v --tb=short"
    
    return run_command(cmd, f"Specific test: {test_file}")

def main():
    parser = argparse.ArgumentParser(description="Run Emphizor integration tests")
    parser.add_argument('--type', choices=['all', 'integration', 'auth', 'database', 'gui'], 
                       default='all', help='Type of tests to run')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--coverage', '-c', action='store_true', help='Run with coverage')
    parser.add_argument('--check-only', action='store_true', help='Only check requirements')
    parser.add_argument('--file', help='Run specific test file')
    parser.add_argument('--function', help='Run specific test function')
    parser.add_argument('--install-deps', action='store_true', help='Install test dependencies')
    
    args = parser.parse_args()
    
    # Check current directory
    if not os.path.exists('base_classes.py'):
        print("ERROR: Please run this script from the Emphizor project root directory")
        sys.exit(1)
    
    # Install dependencies if requested
    if args.install_deps:
        print("Installing test dependencies...")
        if run_command("pip install -r test_requirements.txt", "Installing test dependencies"):
            print("✓ Test dependencies installed successfully")
        else:
            print("✗ Failed to install test dependencies")
            sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("\nTo install test requirements, run:")
        print("pip install -r test_requirements.txt")
        print("\nOr use: python run_tests.py --install-deps")
        sys.exit(1)
    
    # Check test environment
    if not check_test_env():
        print("\nPlease create a test.env file with the following format:")
        print("TEST_USER_EMAIL=test@example.com")
        print("TEST_USER_PASSWORD=testpassword")
        print("TEST_USER_NAME=Test User")
        sys.exit(1)
    
    if args.check_only:
        print("✓ All requirements check passed")
        sys.exit(0)
    
    # Run specific test file
    if args.file:
        success = run_specific_test(args.file, args.function)
        sys.exit(0 if success else 1)
    
    # Run tests
    print(f"\nRunning {args.type} tests...")
    success = run_integration_tests(args.type, args.verbose, args.coverage)
    
    if success:
        print("\n🎉 All tests passed!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 