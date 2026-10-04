# Agent Specification

## Goal

Keep Meesho category managers informed of categories whose month-on-month revenue moves beyond the 8% threshold, while requiring human approval before any message is considered sent.

## Tools

The agent calls:

- `validate_feed` from Part 2 to validate inputs.
- `mom_growth` from Part 2 to calculate month-on-month growth.
- `is_flagged` from Part 2 to classify each growth value.
- The Part 3 prompt/template-fill function to create a stakeholder draft.

## Memory / State

The agent must retain the previous month's validated revenue by category so that the next run can compare the current feed against it. It should also retain the run month and the category-level result used to create each draft.

## Planner

1. Load the monthly revenue feed and run `validate_feed`.
2. If invalid, Hard Stop and report validation errors.
3. If valid, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by `abs(mom_pct)` descending.
6. Draft a message for at most the top 3 flagged categories.
7. Log remaining flagged categories as `suppressed, review manually`.
7b. Log exact-boundary categories in `escalated_categories` without drafting them.
8. Emit one structured JSON object for the run.

## Feedback Loop

Every draft is held for human approval. The mock runner does not send email or call an external service. The output uses `action_taken = "drafted_and_held_for_approval"`.

## Guardrails

### Input guardrail
`validate_feed` must pass before any MoM computation occurs.

### Action guardrail
No message is auto-sent. The runner only drafts and holds messages for approval.

### Output guardrail
Every number in a drafted message must trace back to a Part 1 or Part 2 value. No invented figures are permitted.

## Success and Error Stopping Conditions

**Success:** Drafts are produced, or zero drafts are correctly produced when no category crosses the threshold, and all numbers are traceable.

**Error:** If `validate_feed` returns `False`, the run is a **Hard Stop**. Validation errors are surfaced and no MoM computation is attempted.

## Given-When-Then Agent Specifications

1. **GIVEN** April→May Ethnic Wear revenue moves from 104520.77 to 185107.61, **WHEN** the agent evaluates it, **THEN** MoM growth is 77.1 and the category is flagged.

2. **GIVEN** May→June Beauty & Personal Care revenue moves from 35542.11 to 37559.07, **WHEN** the agent evaluates it, **THEN** MoM growth is 5.67 and the category is not flagged.

3. **GIVEN** previous revenue 100000 and current revenue 108000, **WHEN** the agent evaluates it, **THEN** MoM growth is exactly 8.0 and the category is escalated for human review.

4. **GIVEN** the corrupted feed fixture, **WHEN** the agent validates it, **THEN** validation fails with exactly the three required errors and the workflow Hard Stops.

## Output Contract

Every run emits one JSON object with exactly these top-level keys:

- `run_month`
- `validation_status`
- `validation_errors`
- `flagged_categories`
- `suppressed_categories`
- `escalated_categories`
- `action_taken`
