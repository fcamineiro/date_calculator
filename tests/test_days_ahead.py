#!/usr/bin/env python3
"""
Comprehensive unit tests for days_ahead.py

Tests cover:
- parse_args() function with various argument combinations
- parse_base_date() with valid and invalid inputs
- main() function with positive/negative day offsets
- Custom format strings
- Error handling and SystemExit scenarios
- Edge cases (leap years, year boundaries, large offsets)
"""

import pytest
from datetime import date, datetime
from unittest.mock import patch
from io import StringIO
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from days_ahead import parse_args, parse_base_date, main


class TestParseArgs:
    """Unit tests for the parse_args function."""

    @pytest.mark.unit
    def test_basic_args(self):
        """Test parsing basic required arguments."""
        args = parse_args(['2025-09-10', '30'])
        assert args.base == '2025-09-10'
        assert args.days == 30
        assert args.format == '%Y-%m-%d'

    @pytest.mark.unit
    def test_today_keyword(self):
        """Test parsing with 'today' keyword."""
        args = parse_args(['today', '7'])
        assert args.base == 'today'
        assert args.days == 7

    @pytest.mark.unit
    def test_negative_days(self):
        """Test parsing negative days argument."""
        args = parse_args(['2025-01-15', '-5'])
        assert args.base == '2025-01-15'
        assert args.days == -5

    @pytest.mark.unit
    def test_custom_format_long_flag(self):
        """Test parsing with custom format using --format."""
        args = parse_args(['2025-01-01', '10', '--format', '%d/%m/%Y'])
        assert args.format == '%d/%m/%Y'

    @pytest.mark.unit
    def test_custom_format_short_flag(self):
        """Test parsing with custom format using -f."""
        args = parse_args(['today', '5', '-f', '%B %d, %Y'])
        assert args.format == '%B %d, %Y'

    @pytest.mark.edge_case
    def test_zero_days(self):
        """Test parsing zero days (same date)."""
        args = parse_args(['2025-01-01', '0'])
        assert args.days == 0

    @pytest.mark.edge_case
    def test_large_positive_offset(self):
        """Test parsing very large positive day offset."""
        args = parse_args(['2025-01-01', '1000'])
        assert args.days == 1000

    @pytest.mark.edge_case
    def test_large_negative_offset(self):
        """Test parsing very large negative day offset."""
        args = parse_args(['2025-01-01', '-500'])
        assert args.days == -500


class TestParseBaseDate:
    """Unit tests for the parse_base_date function."""

    @pytest.mark.unit
    def test_valid_iso_date(self):
        """Test parsing valid ISO 8601 date."""
        result = parse_base_date('2025-09-10')
        assert result == date(2025, 9, 10)

    @pytest.mark.unit
    def test_today_lowercase(self):
        """Test parsing 'today' keyword (lowercase)."""
        with patch('days_ahead.date') as mock_date:
            mock_date.today.return_value = date(2025, 1, 9)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
            result = parse_base_date('today')
            assert result == date(2025, 1, 9)

    @pytest.mark.unit
    def test_today_uppercase(self):
        """Test parsing 'TODAY' keyword (uppercase)."""
        with patch('days_ahead.date') as mock_date:
            mock_date.today.return_value = date(2025, 6, 15)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
            result = parse_base_date('TODAY')
            assert result == date(2025, 6, 15)

    @pytest.mark.unit
    def test_now_keyword(self):
        """Test parsing 'now' as alternative to 'today'."""
        with patch('days_ahead.date') as mock_date:
            mock_date.today.return_value = date(2025, 3, 20)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
            result = parse_base_date('now')
            assert result == date(2025, 3, 20)

    @pytest.mark.edge_case
    def test_leap_year_date(self):
        """Test parsing leap year date (Feb 29)."""
        result = parse_base_date('2024-02-29')
        assert result == date(2024, 2, 29)

    @pytest.mark.unit
    def test_invalid_format(self):
        """Test invalid date format raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            parse_base_date('09-10-2025')
        assert "Invalid base date" in str(exc_info.value)

    @pytest.mark.unit
    def test_invalid_month(self):
        """Test invalid month raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            parse_base_date('2025-13-01')
        assert "Invalid base date" in str(exc_info.value)

    @pytest.mark.unit
    def test_invalid_day(self):
        """Test invalid day raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            parse_base_date('2025-02-30')
        assert "Invalid base date" in str(exc_info.value)

    @pytest.mark.edge_case
    def test_completely_invalid_string(self):
        """Test completely invalid string raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            parse_base_date('not-a-date')
        assert "Invalid base date" in str(exc_info.value)


class TestMainFunction:
    """Integration tests for the main function."""

    @pytest.mark.integration
    def test_basic_positive_offset(self):
        """Test main with positive day offset."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-09-10', '30'])
            output = fake_out.getvalue().strip()
            assert output == '2025-10-10'

    @pytest.mark.integration
    def test_basic_negative_offset(self):
        """Test main with negative day offset."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-09-10', '-5'])
            output = fake_out.getvalue().strip()
            assert output == '2025-09-05'

    @pytest.mark.integration
    def test_with_today_keyword(self):
        """Test main with 'today' keyword."""
        with patch('days_ahead.date') as mock_date:
            mock_date.today.return_value = date(2025, 1, 9)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

            with patch('sys.stdout', new=StringIO()) as fake_out:
                main(['today', '7'])
                output = fake_out.getvalue().strip()
                assert output == '2025-01-16'

    @pytest.mark.integration
    def test_custom_format_us_style(self):
        """Test main with custom US date format."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-15', '10', '--format', '%m/%d/%Y'])
            output = fake_out.getvalue().strip()
            assert output == '01/25/2025'

    @pytest.mark.integration
    def test_custom_format_verbose(self):
        """Test main with verbose date format."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-15', '10', '-f', '%B %d, %Y'])
            output = fake_out.getvalue().strip()
            assert output == 'January 25, 2025'

    @pytest.mark.integration
    def test_zero_offset(self):
        """Test main with zero day offset (same date)."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-03-15', '0'])
            output = fake_out.getvalue().strip()
            assert output == '2025-03-15'

    @pytest.mark.integration
    def test_invalid_base_date(self):
        """Test main with invalid base date raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            main(['invalid-date', '10'])
        assert "Invalid base date" in str(exc_info.value)


class TestEdgeCasesAndBoundaries:
    """Edge case and boundary condition tests."""

    @pytest.mark.edge_case
    def test_cross_year_boundary_forward(self):
        """Test crossing year boundary going forward."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2024-12-25', '15'])
            output = fake_out.getvalue().strip()
            assert output == '2025-01-09'

    @pytest.mark.edge_case
    def test_cross_year_boundary_backward(self):
        """Test crossing year boundary going backward."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-05', '-10'])
            output = fake_out.getvalue().strip()
            assert output == '2024-12-26'

    @pytest.mark.edge_case
    def test_leap_year_feb_29(self):
        """Test calculation involving Feb 29 in leap year."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2024-02-28', '1'])
            output = fake_out.getvalue().strip()
            assert output == '2024-02-29'

    @pytest.mark.edge_case
    def test_leap_year_to_non_leap_year(self):
        """Test going from Feb 29 in leap year forward."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2024-02-29', '365'])
            output = fake_out.getvalue().strip()
            assert output == '2025-02-28'

    @pytest.mark.edge_case
    def test_very_large_positive_offset(self):
        """Test very large positive day offset (multiple years)."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2020-01-01', '1826'])  # ~5 years
            output = fake_out.getvalue().strip()
            assert output == '2024-12-31'

    @pytest.mark.edge_case
    def test_very_large_negative_offset(self):
        """Test very large negative day offset."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-01', '-365'])
            output = fake_out.getvalue().strip()
            # 2024 is a leap year, so -365 days from 2025-01-01 is 2024-01-02
            assert output == '2024-01-02'

    @pytest.mark.edge_case
    def test_month_end_boundaries(self):
        """Test various month end boundaries."""
        test_cases = [
            (['2025-01-31', '1'], '2025-02-01'),  # Jan 31 + 1
            (['2025-03-31', '1'], '2025-04-01'),  # Mar 31 + 1
            (['2025-04-30', '1'], '2025-05-01'),  # Apr 30 + 1
        ]

        for args, expected in test_cases:
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main(args)
                output = fake_out.getvalue().strip()
                assert output == expected, f"Failed for {args}"

    @pytest.mark.edge_case
    def test_century_boundary(self):
        """Test crossing century boundary."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['1999-12-31', '1'])
            output = fake_out.getvalue().strip()
            assert output == '2000-01-01'

    @pytest.mark.edge_case
    def test_week_format(self):
        """Test custom format showing day of week."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-01', '8', '-f', '%A, %Y-%m-%d'])
            output = fake_out.getvalue().strip()
            assert 'Thursday' in output
            assert '2025-01-09' in output

    @pytest.mark.edge_case
    def test_day_of_year_format(self):
        """Test custom format showing day of year."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-01', '8', '-f', 'Day %j of %Y'])
            output = fake_out.getvalue().strip()
            assert 'Day 009 of 2025' in output


class TestArgumentValidation:
    """Tests for argument validation and error handling."""

    @pytest.mark.unit
    def test_non_integer_days(self):
        """Test that non-integer days argument is rejected."""
        with pytest.raises(SystemExit):
            parse_args(['2025-01-01', 'not-a-number'])

    @pytest.mark.unit
    def test_missing_required_args(self):
        """Test that missing required arguments raises error."""
        with pytest.raises(SystemExit):
            parse_args(['2025-01-01'])  # Missing days

    @pytest.mark.unit
    def test_missing_all_args(self):
        """Test that missing all arguments raises error."""
        with pytest.raises(SystemExit):
            parse_args([])

    @pytest.mark.unit
    def test_format_without_value(self):
        """Test that --format flag without value raises error."""
        with pytest.raises(SystemExit):
            parse_args(['2025-01-01', '10', '--format'])
