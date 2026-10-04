import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from growth_engine import mom_growth, is_flagged, validate_feed


def test_april_may_ethnic():
    # GIVEN April -> May Ethnic Wear
    # WHEN MoM growth and flag are evaluated
    # THEN 77.1% and flagged
    pct = mom_growth(104520.77, 185107.61)
    assert pct == 77.1
    assert is_flagged(pct) == "flagged"


def test_may_june_beauty():
    # GIVEN May -> June Beauty & Personal Care
    # WHEN evaluated
    # THEN 5.67% and not flagged
    pct = mom_growth(35542.11, 37559.07)
    assert pct == 5.67
    assert is_flagged(pct) == "not_flagged"


def test_exact_boundary():
    # GIVEN a synthetic 8% increase
    # WHEN evaluated
    # THEN it escalates for human review
    pct = mom_growth(100000, 108000)
    assert pct == 8.0
    assert is_flagged(pct) == "escalate_exact_boundary"


def test_corrupted_feed():
    # GIVEN the supplied corrupted feed
    # WHEN validation runs
    # THEN exactly three errors appear in required order
    fixture = os.path.join(os.path.dirname(__file__), "fixtures", "corrupted_feed.csv")
    valid, errors = validate_feed(fixture)

    assert valid is False
    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]


def test_valid_feed():
    fixture = os.path.join(
        os.path.dirname(__file__), "fixtures", "monthly_category_revenue.csv"
    )
    valid, errors = validate_feed(fixture)
    assert valid is True
    assert errors == []


if __name__ == "__main__":
    test_april_may_ethnic()
    test_may_june_beauty()
    test_exact_boundary()
    test_corrupted_feed()
    test_valid_feed()
    print("All Part 2 tests passed.")
