# Date Calculator

A collection of Python CLI utilities for date calculations. This project includes three independent command-line tools for common date arithmetic operations.

## Features

- **Age Calculator** - Interactive tool to calculate age in years and months from a birthdate
- **Days Ahead/Behind** - CLI tool to calculate dates N days ahead or behind from a base date
- **Weeks Ahead/Behind** - CLI tool to calculate dates N weeks ahead or behind from a base date

## Prerequisites

- Python 3.10 or higher

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/date_calculator.git
cd date_calculator
```

2. (Optional) Create and activate a virtual environment:
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Or using standard Python
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

3. (Optional) Install development dependencies for testing:
```bash
uv pip install -e ".[dev]"
# or
pip install -e ".[dev]"
```

## Usage

### Age Calculator

Interactive tool that prompts for a birthdate and calculates age:

```bash
python age_calculator.py
```

**Example:**
```
Enter your date of birth (YYYY-MM-DD): 1990-05-15
You are 35 years and 7 months old.
```

### Days Ahead/Behind

Calculate dates N days ahead or behind from a base date:

```bash
python days_ahead.py <base_date> <days> [--format FORMAT]
```

**Arguments:**
- `base_date`: Date in YYYY-MM-DD format or "today"
- `days`: Number of days (positive for future, negative for past)
- `--format`: (Optional) Custom output format using strftime codes (default: %Y-%m-%d)

**Examples:**
```bash
# 7 days from today
python days_ahead.py today 7
# Output: 2026-01-16

# 30 days from a specific date
python days_ahead.py 2025-09-10 30
# Output: 2025-10-10

# 5 days before a specific date
python days_ahead.py 2025-09-10 -5
# Output: 2025-09-05

# Custom format (e.g., "Month Day, Year")
python days_ahead.py today 14 --format "%B %d, %Y"
# Output: January 23, 2026
```

### Weeks Ahead/Behind

Calculate dates N weeks ahead or behind from a base date:

```bash
python weeks_ahead.py <base_date> <weeks> [--format FORMAT]
```

**Arguments:**
- `base_date`: Date in YYYY-MM-DD format or "today"
- `weeks`: Number of weeks (positive for future, negative for past)
- `--format`: (Optional) Custom output format using strftime codes (default: %Y-%m-%d)

**Examples:**
```bash
# 3 weeks from today
python weeks_ahead.py today 3
# Output: 2026-01-30

# 12 weeks from a specific date
python weeks_ahead.py 2025-09-10 12
# Output: 2025-12-03

# 2 weeks before a specific date
python weeks_ahead.py 2025-09-10 -2
# Output: 2025-08-27

# Custom format (e.g., "Day/Month/Year")
python weeks_ahead.py today 4 --format "%d/%m/%Y"
# Output: 06/02/2026
```

## Testing

The project includes comprehensive unit tests covering all functionality, edge cases, and error handling.

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov
```

Run tests for a specific module:
```bash
pytest tests/test_age_calculator.py
pytest tests/test_days_ahead.py
pytest tests/test_weeks_ahead.py
```

The test suite includes 166+ tests covering:
- Valid input scenarios with various argument combinations
- Edge cases (leap years, month boundaries, century boundaries)
- Error handling (invalid dates, missing arguments, invalid formats)
- Output format verification
- Large offsets (multiple years)

## Project Structure

```
date_calculator/
├── age_calculator.py      # Interactive age calculator
├── days_ahead.py          # CLI tool for day calculations
├── weeks_ahead.py         # CLI tool for week calculations
├── tests/                 # Test suite
│   ├── test_age_calculator.py
│   ├── test_days_ahead.py
│   └── test_weeks_ahead.py
├── pyproject.toml         # Project metadata and dependencies
├── pytest.ini             # Pytest configuration
├── CLAUDE.md              # Project instructions
└── README.md              # This file
```

## Development

This project uses only Python's built-in `datetime` module - no external runtime dependencies are required. The tools are designed as standalone scripts with no shared code or common utilities.

### Development Tools

The project is configured to use modern Python development tools:
- **uv** - Fast package manager (recommended)
- **pytest** - Testing framework with coverage support
- **Built-in datetime** - All date/time operations

## License

This project is provided as-is for educational and practical use.
