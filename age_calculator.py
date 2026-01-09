from datetime import date

def age_years_months(birthdate: date, today: date | None = None) -> tuple[int, int]:
    """
    Return (years, months) of age as of *today*.
    Months counts the extra months beyond the last full birthday,
    so the result is always 0 ≤ months ≤ 11.
    """
    today = today or date.today()
    years  = today.year  - birthdate.year
    months = today.month - birthdate.month

    # If birthday day hasn't occurred yet this month, borrow one month
    if today.day < birthdate.day:
        months -= 1

    if months < 0:          # borrowed past January
        months += 12
        years  -= 1

    return years, months


def prompt_dob() -> date:
    """Prompt the user until a valid YYYY-MM-DD date is entered."""
    while True:
        dob_str = input("Enter your DOB (YYYY-MM-DD): ").strip()
        try:
            year, month, day = map(int, dob_str.split("-"))
            return date(year, month, day)     # raises ValueError on bad dates
        except ValueError:
            print("Please enter a valid date in the form 1990-04-29.")


def main() -> None:
    dob = prompt_dob()
    y, m = age_years_months(dob)
    unit_m = "month"  if m == 1 else "months"
    unit_y = "year"   if y == 1 else "years"
    print(f"You are {y} {unit_y} and {m} {unit_m} old.")


if __name__ == "__main__":
    main()