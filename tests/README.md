# Emphizor Integration Tests

This directory contains comprehensive integration tests for the Emphizor flashcard application, focusing on testing the complete functionality with real-world scenarios using test user credentials.

## Overview

The test suite includes:
- **Core Integration Tests**: Testing the main App class functionality, authentication, and data management
- **GUI Integration Tests**: Testing the GUI components and user interactions
- **Database Integration Tests**: Testing data persistence and database operations
- **Authentication Tests**: Testing user login/signup flows
- **Practice Session Tests**: Testing the spaced repetition functionality

## Setup

### 1. Install Test Dependencies

```bash
pip install -r test_requirements.txt
```

Or use the test runner:
```bash
python run_tests.py --install-deps
```

### 2. Create Test Environment

Create a `test.env` file in the project root with your test credentials:

```env
# Test environment variables for Emphizor integration tests
# These should be test credentials only - NOT production credentials

# Test user credentials
TEST_USER_EMAIL=test@emphizor.com
TEST_USER_PASSWORD=testpassword123
TEST_USER_NAME=Test User

# Additional test user for multi-user testing
TEST_USER_2_EMAIL=test2@emphizor.com
TEST_USER_2_PASSWORD=testpassword456
TEST_USER_2_NAME=Test User 2
```

⚠️ **Important**: Use only test credentials! Never use production credentials in tests.

## Running Tests

### Using the Test Runner (Recommended)

```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --type integration
python run_tests.py --type auth
python run_tests.py --type database
python run_tests.py --type gui

# Run with coverage
python run_tests.py --coverage

# Run specific test file
python run_tests.py --file test_integration.py

# Run specific test function
python run_tests.py --file test_integration.py --function test_login_with_valid_credentials

# Verbose output
python run_tests.py --verbose
```

### Using pytest directly

```bash
# Run all tests
pytest tests/

# Run specific test types
pytest tests/ -m integration
pytest tests/ -m auth
pytest tests/ -m database
pytest tests/ -m gui

# Run with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_integration.py -v

# Run specific test function
pytest tests/test_integration.py::TestAppIntegration::test_login_with_valid_credentials -v
```

## Test Structure

### Test Files

- **`conftest.py`**: Test configuration and fixtures
- **`test_integration.py`**: Core application integration tests
- **`test_gui_integration.py`**: GUI component integration tests
- **`test_database_integration.py`**: Database operation tests

### Test Markers

Tests are marked with the following markers:
- `@pytest.mark.integration`: General integration tests
- `@pytest.mark.auth`: Authentication-related tests
- `@pytest.mark.database`: Database operation tests
- `@pytest.mark.gui`: GUI component tests

### Test Fixtures

Common fixtures available in all tests:
- `test_env`: Test environment variables
- `app`: Fresh App instance
- `test_user`: User instance with sample data
- `sample_cards`: Collection of sample flashcards
- `due_cards`: Cards that are due for review
- `mock_supabase`: Mock Supabase client for testing without API calls

## Test Categories

### 1. Core Integration Tests (`test_integration.py`)

Tests the main application functionality:
- App initialization
- User authentication (login/signup)
- Card management (CRUD operations)
- Practice session simulation
- Data serialization/deserialization
- FSRS scheduler integration
- Error handling

### 2. GUI Integration Tests (`test_gui_integration.py`)

Tests the GUI components:
- Authentication dialog
- Main window initialization
- Card addition through GUI
- Tag management
- Practice dialog flow
- Error handling in GUI
- Auto-save functionality

### 3. Database Integration Tests (`test_database_integration.py`)

Tests data persistence:
- User creation and login with database
- Card data persistence
- Review log persistence
- Scheduler state persistence
- Large dataset handling
- Error handling
- Data integrity

## Mock vs Real Testing

### Mock Testing (Default)
Most tests use mocked Supabase clients to avoid:
- Network dependencies
- Rate limiting
- Database pollution
- Authentication issues

### Real Testing
Some tests can use real Supabase connections:
- Set up test database credentials
- Use separate test environment
- Clean up test data after runs

## Continuous Integration

The test suite is designed to work in CI/CD environments:
- No GUI dependencies for headless testing
- Configurable test credentials
- Comprehensive error reporting
- Coverage reporting

## Test Data Management

### Sample Data
Tests use predefined sample data:
- Sample flashcards with various topics
- Test users with different configurations
- Mock review logs and scheduler states

### Test Isolation
Each test runs in isolation:
- Fresh app instances
- Clean test data
- No side effects between tests

## Coverage

Generate coverage reports:
```bash
python run_tests.py --coverage
```

This generates:
- Terminal coverage report
- HTML coverage report in `htmlcov/index.html`

## Troubleshooting

### Common Issues

1. **Missing test.env**: Create the test environment file
2. **Import errors**: Install test dependencies
3. **Authentication failures**: Check test credentials
4. **GUI tests failing**: Ensure Qt dependencies are installed
5. **Timeout errors**: Check network connection or use mock tests

### Debug Mode

For debugging failing tests:
```bash
pytest tests/ -v --tb=long --capture=no
```

### Test Specific Issues

For specific test failures:
```bash
pytest tests/test_integration.py::TestAppIntegration::test_login_with_valid_credentials -v -s
```

## Best Practices

1. **Use Mock Testing**: Prefer mocked tests for reliability
2. **Test Isolation**: Each test should be independent
3. **Descriptive Names**: Use clear, descriptive test names
4. **Comprehensive Coverage**: Test both success and failure scenarios
5. **Environment Separation**: Keep test and production environments separate

## Contributing

When adding new tests:

1. Follow the existing test structure
2. Use appropriate test markers
3. Add comprehensive documentation
4. Test both success and failure scenarios
5. Update this README if adding new test categories

## Security Notes

- Never commit test credentials to version control
- Use separate test databases/accounts
- Regularly rotate test credentials
- Monitor test environment for any security issues 