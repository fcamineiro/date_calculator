#!/usr/bin/env python3
"""
Comprehensive unit tests for age_calculator.py

Tests cover:
- age_years_months() function with various date combinations
- Edge cases (leap years, month boundaries, same dates)
- Interactive prompt functionality
- Error handling for invalid dates
- Main function integration
"""

import pytest
from datetime import date
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from age_calculator import age_years_months, prompt_dob, main


class TestAgeYearsMonths:
    """Unit tests for the age_years_months function."""

    @pytest.mark.unit
    def test_basic_age_calculation(self):
        """Test basic age calculation with no month complications."""
        birthdate = date(2000, 1, 15)
        today = date(2025, 1, 15)
        years, months = age_years_months(birthdate, today)
        assert years == 25
        assert months == 0

    @pytest.mark.unit
    def test_age_with_months(self):
        """Test age calculation with additional months."""
        birthdate = date(2000, 3, 10)
        today = date(2025, 7, 10)
        years, months = age_years_months(birthdate, today)
        assert years == 25
        assert months == 4

    @pytest.mark.unit
    def test_birthday_not_yet_occurred_this_month(self):
        """Test when birthday day hasn't occurred yet this month."""
        birthdate = date(2000, 5, 25)
        today = date(2025, 5, 20)
        years, months = age_years_months(birthdate, today)
        assert years == 24
        assert months == 11

    @pytest.mark.unit
    def test_birthday_not_yet_occurred_this_year(self):
        """Test when birthday hasn't occurred yet this year."""
        birthdate = date(2000, 10, 15)
        today = date(2025, 3, 20)
        years, months = age_years_months(birthdate, today)
        assert years == 24
        assert months == 5

    @pytest.mark.edge_case
    def test_leap_year_birthday(self):
        """Test with leap year birthday (Feb 29)."""
        birthdate = date(2000, 2, 29)
        today = date(2025, 3, 1)
        years, months = age_years_months(birthdate, today)
        assert years == 25
        assert months == 0

    @pytest.mark.edge_case
    def test_same_date(self):
        """Test when birthdate equals today (newborn)."""
        birthdate = date(2025, 1, 1)
        today = date(2025, 1, 1)
        years, months = age_years_months(birthdate, today)
        assert years == 0
        assert months == 0

    @pytest.mark.edge_case
    def test_one_month_old(self):
        """Test exactly one month old."""
        birthdate = date(2024, 12, 1)
        today = date(2025, 1, 1)
        years, months = age_years_months(birthdate, today)
        assert years == 0
        assert months == 1

    @pytest.mark.edge_case
    def test_month_borrowing_across_year_boundary(self):
        """Test month borrowing when months go negative across year boundary."""
        birthdate = date(2000, 12, 25)
        today = date(2025, 1, 10)
        years, months = age_years_months(birthdate, today)
        assert years == 24
        assert months == 0

    @pytest.mark.unit
    def test_uses_today_when_no_date_provided(self):
        """Test that function uses date.today() when today parameter is None."""
        birthdate = date(2000, 1, 1)
        with patch('age_calculator.date') as mock_date:
            mock_date.today.return_value = date(2025, 6, 15)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
            years, months = age_years_months(birthdate, None)
            # Should use mocked today
            assert years == 25
            assert months == 5

    @pytest.mark.edge_case
    def test_end_of_month_boundaries(self):
        """Test with end-of-month dates (e.g., Jan 31 to Feb 28)."""
        birthdate = date(2000, 1, 31)
        today = date(2025, 2, 28)
        years, months = age_years_months(birthdate, today)
        # Feb 28 < Jan 31 (day-wise), so we haven't hit the birthday yet
        assert years == 25
        assert months == 0

    @pytest.mark.unit
    def test_multiple_years_with_months(self):
        """Test calculation spanning multiple years with months."""
        birthdate = date(1990, 4, 15)
        today = date(2025, 9, 20)
        years, months = age_years_months(birthdate, today)
        assert years == 35
        assert months == 5


class TestPromptDob:
    """Unit tests for the prompt_dob function."""

    @pytest.mark.unit
    @patch('builtins.input', return_value='1990-04-29')
    def test_valid_date_input(self, mock_input):
        """Test valid date input on first attempt."""
        result = prompt_dob()
        assert result == date(1990, 4, 29)
        assert mock_input.call_count == 1

    @pytest.mark.unit
    @patch('builtins.input', side_effect=['invalid', '1990-13-01', '1990-04-29'])
    @patch('builtins.print')
    def test_invalid_then_valid_input(self, mock_print, mock_input):
        """Test retry logic with invalid inputs before valid one."""
        result = prompt_dob()
        assert result == date(1990, 4, 29)
        assert mock_input.call_count == 3
        # Should print error message twice
        assert mock_print.call_count == 2

    @pytest.mark.edge_case
    @patch('builtins.input', side_effect=['not-a-date', '2000-02-30', '2000-02-29'])
    @patch('builtins.print')
    def test_various_invalid_formats(self, mock_print, mock_input):
        """Test handling of various invalid date formats."""
        result = prompt_dob()
        assert result == date(2000, 2, 29)
        assert mock_input.call_count == 3

    @pytest.mark.edge_case
    @patch('builtins.input', return_value='  2000-01-01  ')
    def test_whitespace_handling(self, mock_input):
        """Test that whitespace is stripped from input."""
        result = prompt_dob()
        assert result == date(2000, 1, 1)


class TestMainFunction:
    """Integration tests for the main function."""

    @pytest.mark.integration
    @patch('builtins.input', return_value='2000-01-01')
    @patch('age_calculator.date')
    def test_main_output_singular_units(self, mock_date, mock_input):
        """Test main function output with singular year and month."""
        mock_date.today.return_value = date(2001, 2, 1)
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            assert "1 year" in output
            assert "1 month" in output
            assert "years" not in output.replace("1 year", "")  # No plural

    @pytest.mark.integration
    @patch('builtins.input', return_value='2000-01-01')
    @patch('age_calculator.date')
    def test_main_output_plural_units(self, mock_date, mock_input):
        """Test main function output with plural years and months."""
        mock_date.today.return_value = date(2025, 6, 15)
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            assert "25 years" in output
            assert "5 months" in output

    @pytest.mark.integration
    @patch('builtins.input', return_value='2000-01-01')
    @patch('age_calculator.date')
    def test_main_output_zero_months(self, mock_date, mock_input):
        """Test main function output with zero months."""
        mock_date.today.return_value = date(2025, 1, 1)
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            assert "25 years" in output
            assert "0 months" in output

    @pytest.mark.integration
    @patch('builtins.input', side_effect=['invalid-date', '1995-06-15'])
    @patch('age_calculator.date')
    def test_main_with_retry(self, mock_date, mock_input):
        """Test main function handles retry from prompt_dob."""
        mock_date.today.return_value = date(2025, 9, 20)
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            assert "30 years" in output
            assert "3 months" in output


class TestEdgeCasesAndBoundaries:
    """Additional edge case and boundary condition tests."""

    @pytest.mark.edge_case
    def test_century_boundary(self):
        """Test age calculation across century boundary."""
        birthdate = date(1999, 12, 31)
        today = date(2000, 1, 1)
        years, months = age_years_months(birthdate, today)
        assert years == 0
        assert months == 0

    @pytest.mark.edge_case
    def test_very_old_age(self):
        """Test with very old age (100+ years)."""
        birthdate = date(1900, 5, 15)
        today = date(2025, 7, 20)
        years, months = age_years_months(birthdate, today)
        assert years == 125
        assert months == 2

    @pytest.mark.edge_case
    def test_all_month_boundaries(self):
        """Test birthdate on last day of each month."""
        test_cases = [
            (date(2000, 1, 31), date(2025, 2, 28), 25, 0),  # Jan 31 birthday
            (date(2000, 3, 31), date(2025, 4, 30), 25, 0),  # Mar 31 birthday
            (date(2000, 4, 30), date(2025, 5, 29), 25, 0), # Apr 30 birthday
        ]

        for birthdate, today, expected_years, expected_months in test_cases:
            years, months = age_years_months(birthdate, today)
            assert years == expected_years, f"Failed for {birthdate} to {today}"
            assert months == expected_months, f"Failed for {birthdate} to {today}"

    @pytest.mark.edge_case
    def test_leap_year_non_leap_year(self):
        """Test Feb 29 birthday in non-leap year."""
        birthdate = date(2000, 2, 29)
        today = date(2025, 2, 28)
        years, months = age_years_months(birthdate, today)
        # Feb 28 < Feb 29 (day-wise), birthday hasn't happened yet
        assert years == 24
        assert months == 11
