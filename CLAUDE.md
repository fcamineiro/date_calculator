# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python date calculator utility collection with three independent command-line tools:

1. **age_calculator.py** - Interactive age calculator that prompts for a birth date and calculates age in years and months
2. **days_ahead.py** - CLI tool to calculate dates N days ahead or behind from a base date
3. **weeks_ahead.py** - CLI tool to calculate dates N weeks ahead or behind from a base date

## Running the Tools

```bash
# Age Calculator (interactive)
python age_calculator.py

# Days Calculator
python days_ahead.py YYYY-MM-DD N [--format FMT]
python days_ahead.py today 7
python days_ahead.py 2025-09-10 30
python days_ahead.py 2025-09-10 -5  # 5 days before

# Weeks Calculator
python weeks_ahead.py YYYY-MM-DD N [--format FMT]
python weeks_ahead.py today 3
python weeks_ahead.py 2025-09-10 12
python weeks_ahead.py 2025-09-10 -2  # 2 weeks before
```

## Testing

The project includes comprehensive unit tests for all three utilities using pytest:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov

# Run tests for a specific module
pytest tests/test_age_calculator.py
pytest tests/test_days_ahead.py
pytest tests/test_weeks_ahead.py
```

### Test Coverage

- **tests/test_age_calculator.py**: Tests the `age_years_months()` function including edge cases like month borrowing, leap years, and boundary conditions
- **tests/test_days_ahead.py**: Tests date arithmetic with positive/negative day offsets, "today" keyword, and custom formatting
- **tests/test_weeks_ahead.py**: Tests date arithmetic with positive/negative week offsets, "today" keyword, and custom formatting

### Development Setup

Install development dependencies (requires uv):

```bash
uv pip install -e ".[dev]"
```

## Architecture

All scripts are standalone modules with no shared dependencies or common utilities. Each can be run independently:

- **age_calculator.py**: Uses `date.today()` as reference point, calculates age with proper month borrowing logic when the birthday hasn't occurred yet in the current month
- **days_ahead.py**: Uses `timedelta(days=N)` for date arithmetic, supports custom output formatting via strftime
- **weeks_ahead.py**: Uses `timedelta(weeks=N)` for date arithmetic, supports custom output formatting via strftime

The core age calculation logic in `age_years_months()` handles edge cases like:
- Month borrowing when current day < birth day
- Year adjustment when months go negative (borrowed past January)

All tools use Python's built-in `datetime` module exclusively - no external dependencies.
