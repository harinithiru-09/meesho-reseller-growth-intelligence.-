# Reusable Prompt Pack

## Trigger

Start this prompt only when a category's `is_flagged` result is exactly `"flagged"`.

## Input list

The template requires:

- `{category}`
- `{previous_revenue}`
- `{current_revenue}`
- `{mom_pct}`
- `{month}`
- `{prev_month}`

## Prompt

You are preparing a short stakeholder update for a Meesho regional manager.

Use the supplied values only:

- Category: `{category}`
- Previous month: `{prev_month}`
- Current month: `{month}`
- Previous revenue: `{previous_revenue}`
- Current revenue: `{current_revenue}`
- MoM change: `{mom_pct}%`

Write the update using exactly this structure:

1. **Context** — state what category and period are being measured.
2. **Insight — Fact** — state the supplied MoM percentage exactly.
3. **Implication — Hypothesis/Action** — give a specific next step. If you propose a cause, label it as a hypothesis because the supplied revenue data alone does not prove causation.

Do not invent or calculate any additional number. Do not introduce any number that is not one of the supplied placeholders. Keep the message concise and suitable for a regional manager.

## Checklist

Before the draft is released for human review:

- Check that every numeric value in the draft matches a supplied placeholder exactly.
- Check that the category and month names match the supplied inputs.
- Check that factual observations are labeled as facts and proposed causes are labeled as hypotheses.
- Check that the recommendation names a concrete action rather than saying only "look into it."
- Check that no raw reseller name appears if reseller-level information is included.
- Check that the message is a draft only and is held for human approval.
