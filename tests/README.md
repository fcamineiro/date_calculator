# Test Suite for Date Calculator

This directory contains comprehensive unit and integration tests for all three CLI tools in the date calculator project.

## Test Files

- **test_age_calculator.py** - Tests for age_calculator.py (56 tests)
- **test_days_ahead.py** - Tests for days_ahead.py (52 tests)
- **test_weeks_ahead.py** - Tests for weeks_ahead.py (58 tests)

## Prerequisites

This project uses `uv` for dependency management. Make sure you have `uv` installed:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

Install the test dependencies using uv:

```bash
# Install dev dependencies (includes pytest and pytest-cov)
uv pip install -e ".[dev]"
```

Or install pytest directly:

```bash
uv pip install pytest pytest-cov
```

## Running Tests

### Run All Tests

```bash
# Using pytest directly
pytest

# Or with verbose output
pytest -v

# Using uv to run pytest
uv run pytest
```

### Run Specific Test File

```bash
# Test only age_calculator.py
pytest tests/test_age_calculator.py

# Test only days_ahead.py
pytest tests/test_days_ahead.py

# Test only weeks_ahead.py
pytest tests/test_weeks_ahead.py
```

### Run Tests by Category

The tests are marked with custom markers:

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only edge case tests
pytest -m edge_case
```

### Run Specific Test Class or Function

```bash
# Run a specific test class
pytest tests/test_age_calculator.py::TestAgeYearsMonths

# Run a specific test function
pytest tests/test_days_ahead.py::TestMainFunction::test_basic_positive_offset
```

### Run with Coverage

```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# View coverage in terminal
pytest --cov=. --cov-report=term-missing

# Generate both HTML and terminal reports
pytest --cov=. --cov-report=html --cov-report=term-missing
```

The HTML coverage report will be generated in `htmlcov/index.html`.

## Test Organization

Each test file is organized into logical test classes:

### test_age_calculator.py
- `TestAgeYearsMonths` - Tests for the age calculation function
- `TestPromptDob` - Tests for the date input prompt
- `TestMainFunction` - Integration tests for the main function
- `TestEdgeCasesAndBoundaries` - Edge cases and boundary conditions

### test_days_ahead.py
- `TestParseArgs` - Tests for argument parsing
- `TestParseBaseDate` - Tests for date parsing logic
- `TestMainFunction` - Integration tests for the main function
- `TestEdgeCasesAndBoundaries` - Edge cases and boundary conditions
- `TestArgumentValidation` - Argument validation and error handling

### test_weeks_ahead.py
- `TestParseArgs` - Tests for argument parsing
- `TestParseBaseDate` - Tests for date parsing logic
- `TestMainFunction` - Integration tests for the main function
- `TestEdgeCasesAndBoundaries` - Edge cases and boundary conditions
- `TestArgumentValidation` - Argument validation and error handling
- `TestWeekCalculations` - Specific week calculation accuracy tests

## Test Coverage

The test suite covers:

- ✓ Valid input scenarios with various argument combinations
- ✓ Edge cases (leap years, month boundaries, century boundaries)
- ✓ Error handling (invalid dates, missing arguments, invalid formats)
- ✓ SystemExit codes and error messages
- ✓ Output format verification
- ✓ Custom format strings
- ✓ Positive and negative offsets
- ✓ "today" and "now" keyword handling
- ✓ Large offsets (multiple years)
- ✓ Interactive prompts with retry logic

## Continuous Integration

To run tests in CI/CD pipelines:

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Run tests with coverage and fail if coverage is below threshold
pytest --cov=. --cov-fail-under=80 --cov-report=term-missing
```

## Writing New Tests

When adding new tests, follow these guidelines:

1. Use descriptive test names that explain what is being tested
2. Add appropriate markers (`@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.edge_case`)
3. Include docstrings explaining the test purpose
4. Use fixtures for common test data
5. Mock external dependencies (stdin, stdout, date.today())
6. Ensure tests are isolated and can run in any order

Example:

```python
@pytest.mark.unit
def test_my_new_feature(self):
    """Test description explaining what this test validates."""
    # Arrange
    input_data = "test-value"

    # Act
    result = my_function(input_data)

    # Assert
    assert result == expected_value
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure the parent directory is in the Python path. The test files automatically add it:

```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Pytest Not Found

If `pytest` is not found, install it using uv:

```bash
uv pip install pytest
```

### Tests Failing Locally

Make sure you're running tests from the project root directory:

```bash
cd /path/to/date_calculator
pytest
```

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [uv Documentation](https://github.com/astral-sh/uv)
