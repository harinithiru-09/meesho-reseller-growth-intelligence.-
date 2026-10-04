import csv
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART2_DIR = os.path.join(BASE_DIR, "part2_engine")
PART3_DIR = os.path.join(BASE_DIR, "part3_narrative")
sys.path.insert(0, PART2_DIR)
sys.path.insert(0, PART3_DIR)

from growth_engine import validate_feed, mom_growth, is_flagged


def fill_narrative(category, previous_revenue, current_revenue, mom_pct, month, prev_month):
    return (
        f"Context: {category} revenue is being compared between {prev_month} and {month}. "
        f"Insight — Fact: {category} revenue changed by {mom_pct}% MoM from "
        f"{prev_month} to {month}. "
        f"Implication — Hypothesis / Action: The supplied revenue data does not prove the cause. "
        f"Review {category} order activity and reseller contribution before deciding the next action."
    )


def load_feed(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    valid, errors = validate_feed(current_month_csv)

    result = {
        "run_month": month,
        "validation_status": "valid" if valid else "invalid",
        "validation_errors": errors,
        "flagged_categories": [],
        "suppressed_categories": [],
        "escalated_categories": [],
        "action_taken": "drafted_and_held_for_approval" if valid else "hard_stop",
    }

    if not valid:
        return result

    previous_rows = load_feed(previous_month_csv)
    current_rows = load_feed(current_month_csv)

    previous = {row["category"]: float(row["revenue"]) for row in previous_rows}
    current = {row["category"]: float(row["revenue"]) for row in current_rows}

    evaluations = []

    for category, current_revenue in current.items():
        previous_revenue = previous[category]
        pct = mom_growth(previous_revenue, current_revenue)
        status = is_flagged(pct)

        evaluations.append({
            "category": category,
            "mom_pct": pct,
            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
            "status": status,
        })

    flagged = [x for x in evaluations if x["status"] == "flagged"]
    flagged.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)

    exact_boundary = [x for x in evaluations if x["status"] == "escalate_exact_boundary"]
    result["escalated_categories"] = [x["category"] for x in exact_boundary]

    top_three = flagged[:3]
    suppressed = flagged[3:]

    for item in top_three:
        message = fill_narrative(
            item["category"],
            item["previous_revenue"],
            item["current_revenue"],
            item["mom_pct"],
            month,
            "April" if month == "May" else "May",
        )
        result["flagged_categories"].append({
            "category": item["category"],
            "mom_pct": item["mom_pct"],
            "previous_revenue": item["previous_revenue"],
            "current_revenue": item["current_revenue"],
            "drafted": True,
            "message": message,
        })

    result["suppressed_categories"] = [x["category"] for x in suppressed]
    return result


if __name__ == "__main__":
    # Example:
    # python part4_agent/mock_agent_runner.py May \
    #   part2_engine/fixtures/april.csv part2_engine/fixtures/may.csv
    if len(sys.argv) != 4:
        print("Usage: python mock_agent_runner.py <month> <previous_csv> <current_csv>")
        raise SystemExit(1)

    output = run(sys.argv[1], sys.argv[2], sys.argv[3])
    print(json.dumps(output, indent=2))
