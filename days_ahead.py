#!/usr/bin/env python3
"""
days_ahead.py — add or subtract N days from a given date.

Usage:
  python days_ahead.py YYYY-MM-DD N [--format FMT]
  python days_ahead.py today N [--format FMT]

Examples:
  python days_ahead.py 2025-09-10 30        # -> 2025-10-10
  python days_ahead.py today 7              # -> (today + 7 days)

Notes:
- Negative N works to go backwards (e.g., -5 means 5 days before).
- The default output format is ISO 8601 (%Y-%m-%d).
"""

import argparse
import sys
from datetime import date, datetime, timedelta


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Compute a date N days ahead (or behind) from a base date.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python days_ahead.py 2025-09-10 30\n"
            "  python days_ahead.py today 7\n"
        ),
    )
    parser.add_argument("base", help='Base date in YYYY-MM-DD or "today"')
    parser.add_argument(
        "days", type=int, help="Number of days to add (negative to subtract)"
    )
    parser.add_argument(
        "--format",
        "-f",
        default="%Y-%m-%d",
        help="Output strftime format (default: %%Y-%%m-%%d)",
    )
    return parser.parse_args(argv)


def parse_base_date(s: str) -> date:
    if s.lower() in {"today", "now"}:
        return date.today()
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError as e:
        raise SystemExit(
            f"Invalid base date '{s}'. Expected YYYY-MM-DD or 'today'."
        ) from e


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    base_dt = parse_base_date(args.base)
    result = base_dt + timedelta(days=args.days)

    fmt = args.format
    try:
        print(result.strftime(fmt))
    except Exception:
        # Avoid referencing args.format here again (could be missing/invalid on some platforms)
        raise SystemExit("Invalid format string supplied to --format/-f.")


if __name__ == "__main__":
    main()
