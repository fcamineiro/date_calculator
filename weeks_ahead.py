#!/usr/bin/env python3
"""
weeksahead.py — add or subtract N weeks from a given date.

Usage:
  python weeksahead.py YYYY-MM-DD N [--format FMT]
  python weeksahead.py today N [--format FMT]

Examples:
  python weeksahead.py 2025-09-10 12        # -> 2025-12-03
  python weeksahead.py today 3              # -> (today + 21 days)

Notes:
- Negative N works to go backwards (e.g., -2 means 2 weeks before).
- The default output format is ISO 8601 (%Y-%m-%d).
"""

import argparse
import sys
from datetime import date, datetime, timedelta


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Compute a date N weeks ahead (or behind) from a base date.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python weeksahead.py 2025-09-10 12\n"
            "  python weeksahead.py today 3\n"
        ),
    )
    parser.add_argument("base", help='Base date in YYYY-MM-DD or "today"')
    parser.add_argument(
        "weeks", type=int, help="Number of weeks to add (negative to subtract)"
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
    result = base_dt + timedelta(weeks=args.weeks)

    fmt = args.format
    try:
        print(result.strftime(fmt))
    except Exception:
        # Avoid referencing args.format here again (could be missing/invalid on some platforms)
        raise SystemExit("Invalid format string supplied to --format/-f.")


if __name__ == "__main__":
    main()
