#!/usr/bin/env python3
"""
Comprehensive unit tests for weeks_ahead.py

Tests cover:
- parse_args() function with various argument combinations
- parse_base_date() with valid and invalid inputs
- main() function with positive/negative week offsets
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

from weeks_ahead import parse_args, parse_base_date, main


class TestParseArgs:
    """Unit tests for the parse_args function."""

    @pytest.mark.unit
    def test_basic_args(self):
        """Test parsing basic required arguments."""
        args = parse_args(['2025-09-10', '12'])
        assert args.base == '2025-09-10'
        assert args.weeks == 12
        assert args.format == '%Y-%m-%d'

    @pytest.mark.unit
    def test_today_keyword(self):
        """Test parsing with 'today' keyword."""
        args = parse_args(['today', '3'])
        assert args.base == 'today'
        assert args.weeks == 3

    @pytest.mark.unit
    def test_negative_weeks(self):
        """Test parsing negative weeks argument."""
        args = parse_args(['2025-01-15', '-2'])
        assert args.base == '2025-01-15'
        assert args.weeks == -2

    @pytest.mark.unit
    def test_custom_format_long_flag(self):
        """Test parsing with custom format using --format."""
        args = parse_args(['2025-01-01', '4', '--format', '%d/%m/%Y'])
        assert args.format == '%d/%m/%Y'

    @pytest.mark.unit
    def test_custom_format_short_flag(self):
        """Test parsing with custom format using -f."""
        args = parse_args(['today', '2', '-f', '%B %d, %Y'])
        assert args.format == '%B %d, %Y'

    @pytest.mark.edge_case
    def test_zero_weeks(self):
        """Test parsing zero weeks (same date)."""
        args = parse_args(['2025-01-01', '0'])
        assert args.weeks == 0

    @pytest.mark.edge_case
    def test_large_positive_offset(self):
        """Test parsing very large positive week offset."""
        args = parse_args(['2025-01-01', '52'])
        assert args.weeks == 52

    @pytest.mark.edge_case
    def test_large_negative_offset(self):
        """Test parsing very large negative week offset."""
        args = parse_args(['2025-01-01', '-26'])
        assert args.weeks == -26


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
        with patch('weeks_ahead.date') as mock_date:
            mock_date.today.return_value = date(2025, 1, 9)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
            result = parse_base_date('today')
            assert result == date(2025, 1, 9)

    @pytest.mark.unit
    def test_today_uppercase(self):
        """Test parsing 'TODAY' keyword (uppercase)."""
        with patch('weeks_ahead.date') as mock_date:
            mock_date.today.return_value = date(2025, 6, 15)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
            result = parse_base_date('TODAY')
            assert result == date(2025, 6, 15)

    @pytest.mark.unit
    def test_now_keyword(self):
        """Test parsing 'now' as alternative to 'today'."""
        with patch('weeks_ahead.date') as mock_date:
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
        """Test main with positive week offset."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-09-10', '12'])
            output = fake_out.getvalue().strip()
            assert output == '2025-12-03'

    @pytest.mark.integration
    def test_basic_negative_offset(self):
        """Test main with negative week offset."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-09-10', '-2'])
            output = fake_out.getvalue().strip()
            assert output == '2025-08-27'

    @pytest.mark.integration
    def test_with_today_keyword(self):
        """Test main with 'today' keyword."""
        with patch('weeks_ahead.date') as mock_date:
            mock_date.today.return_value = date(2025, 1, 9)
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

            with patch('sys.stdout', new=StringIO()) as fake_out:
                main(['today', '3'])
                output = fake_out.getvalue().strip()
                assert output == '2025-01-30'

    @pytest.mark.integration
    def test_custom_format_us_style(self):
        """Test main with custom US date format."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-15', '2', '--format', '%m/%d/%Y'])
            output = fake_out.getvalue().strip()
            assert output == '01/29/2025'

    @pytest.mark.integration
    def test_custom_format_verbose(self):
        """Test main with verbose date format."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-15', '2', '-f', '%B %d, %Y'])
            output = fake_out.getvalue().strip()
            assert output == 'January 29, 2025'

    @pytest.mark.integration
    def test_zero_offset(self):
        """Test main with zero week offset (same date)."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-03-15', '0'])
            output = fake_out.getvalue().strip()
            assert output == '2025-03-15'

    @pytest.mark.integration
    def test_invalid_base_date(self):
        """Test main with invalid base date raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            main(['invalid-date', '4'])
        assert "Invalid base date" in str(exc_info.value)


class TestEdgeCasesAndBoundaries:
    """Edge case and boundary condition tests."""

    @pytest.mark.edge_case
    def test_cross_year_boundary_forward(self):
        """Test crossing year boundary going forward."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2024-12-25', '2'])  # 2 weeks = 14 days
            output = fake_out.getvalue().strip()
            assert output == '2025-01-08'

    @pytest.mark.edge_case
    def test_cross_year_boundary_backward(self):
        """Test crossing year boundary going backward."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-05', '-2'])
            output = fake_out.getvalue().strip()
            assert output == '2024-12-22'

    @pytest.mark.edge_case
    def test_leap_year_handling(self):
        """Test calculation involving leap year."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2024-02-15', '2'])  # 2 weeks forward
            output = fake_out.getvalue().strip()
            assert output == '2024-02-29'

    @pytest.mark.edge_case
    def test_one_year_in_weeks(self):
        """Test approximately one year (52 weeks)."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2024-01-01', '52'])
            output = fake_out.getvalue().strip()
            assert output == '2024-12-30'

    @pytest.mark.edge_case
    def test_two_years_in_weeks(self):
        """Test approximately two years (104 weeks)."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2023-01-01', '104'])
            output = fake_out.getvalue().strip()
            assert output == '2024-12-29'

    @pytest.mark.edge_case
    def test_very_large_negative_offset(self):
        """Test very large negative week offset."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-12-31', '-52'])
            output = fake_out.getvalue().strip()
            assert output == '2025-01-01'

    @pytest.mark.edge_case
    def test_month_boundary_transitions(self):
        """Test various month boundary transitions."""
        test_cases = [
            (['2025-01-29', '1'], '2025-02-05'),  # Jan to Feb
            (['2025-02-26', '1'], '2025-03-05'),  # Feb to Mar
            (['2025-04-30', '1'], '2025-05-07'),  # Apr to May
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
            main(['1999-12-29', '1'])  # 1 week = 7 days
            output = fake_out.getvalue().strip()
            assert output == '2000-01-05'

    @pytest.mark.edge_case
    def test_week_format(self):
        """Test custom format showing day of week."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-01', '1', '-f', '%A, %Y-%m-%d'])
            output = fake_out.getvalue().strip()
            assert 'Wednesday' in output
            assert '2025-01-08' in output

    @pytest.mark.edge_case
    def test_quarter_year_offset(self):
        """Test 13 weeks (one quarter) offset."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-01', '13'])
            output = fake_out.getvalue().strip()
            assert output == '2025-04-02'


class TestArgumentValidation:
    """Tests for argument validation and error handling."""

    @pytest.mark.unit
    def test_non_integer_weeks(self):
        """Test that non-integer weeks argument is rejected."""
        with pytest.raises(SystemExit):
            parse_args(['2025-01-01', 'not-a-number'])

    @pytest.mark.unit
    def test_missing_required_args(self):
        """Test that missing required arguments raises error."""
        with pytest.raises(SystemExit):
            parse_args(['2025-01-01'])  # Missing weeks

    @pytest.mark.unit
    def test_missing_all_args(self):
        """Test that missing all arguments raises error."""
        with pytest.raises(SystemExit):
            parse_args([])

    @pytest.mark.unit
    def test_format_without_value(self):
        """Test that --format flag without value raises error."""
        with pytest.raises(SystemExit):
            parse_args(['2025-01-01', '4', '--format'])


class TestWeekCalculations:
    """Specific tests for week calculation accuracy."""

    @pytest.mark.unit
    def test_one_week_equals_seven_days(self):
        """Verify 1 week = 7 days."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-01', '1'])
            output = fake_out.getvalue().strip()
            assert output == '2025-01-08'

    @pytest.mark.unit
    def test_four_weeks_equals_28_days(self):
        """Verify 4 weeks = 28 days."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-01', '4'])
            output = fake_out.getvalue().strip()
            assert output == '2025-01-29'

    @pytest.mark.unit
    def test_negative_one_week(self):
        """Verify -1 week = -7 days."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-01-15', '-1'])
            output = fake_out.getvalue().strip()
            assert output == '2025-01-08'

    @pytest.mark.unit
    def test_negative_four_weeks(self):
        """Verify -4 weeks = -28 days."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-02-01', '-4'])
            output = fake_out.getvalue().strip()
            assert output == '2025-01-04'

    @pytest.mark.edge_case
    def test_weeks_across_february_leap_year(self):
        """Test weeks calculation across February in leap year."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2024-02-15', '4'])  # Should land after Feb 29
            output = fake_out.getvalue().strip()
            assert output == '2024-03-14'

    @pytest.mark.edge_case
    def test_weeks_across_february_non_leap_year(self):
        """Test weeks calculation across February in non-leap year."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['2025-02-15', '4'])  # Feb has only 28 days
            output = fake_out.getvalue().strip()
            assert output == '2025-03-15'
