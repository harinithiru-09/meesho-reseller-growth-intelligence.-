import csv


def mom_growth(previous: float, current: float) -> float:
    """Return Month-on-Month growth percentage rounded to 2 decimals."""
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """Classify a MoM percentage using a strict 8% boundary."""
    if abs(mom_pct) > threshold:
        return "flagged"
    if abs(mom_pct) < threshold:
        return "not_flagged"
    return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """Validate month/category/revenue/n_orders CSV input."""
    errors = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            month = row.get("month", "")
            category = row.get("category", "")
            revenue = row.get("revenue", "")

            if category == "":
                errors.append(f"line {line_no}: missing category (month={month})")

            if revenue == "":
                errors.append(f"line {line_no}: missing revenue (category={category})")
            else:
                try:
                    revenue_value = float(revenue)
                except ValueError:
                    errors.append(f"line {line_no}: revenue not numeric: {revenue!r}")
                else:
                    if revenue_value < 0:
                        errors.append(
                            f"line {line_no}: negative revenue ({revenue_value}) for category={category}"
                        )

    return (len(errors) == 0, errors)
