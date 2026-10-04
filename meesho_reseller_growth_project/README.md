# Meesho Reseller Growth & Alert Intelligence Pipeline

A fully offline, deterministic project implementing four connected stages:

**Part 1 SQL → Part 2 Guardrails/Growth Engine → Part 3 Reliable Narrative → Part 4 Guarded Agent Runner**

## Requirements

- Python 3.10+
- SQLite (Python's built-in `sqlite3` is enough)
- Optional: `pytest` for test discovery

No API key or paid service is required.

## 1. Generate the dataset

From the repository root:

```bash
python data/generate_dataset.py
```

This creates:

- `data/resellers.csv` — 24 resellers
- `data/orders.csv` — 900 orders
- `data/meesho_reseller.db` — SQLite database

The generator uses seed 42 and must not be changed.

## 2. Run Part 1

The SQL queries are in:

```text
part1_sql/queries.sql
```

Example:

```bash
sqlite3 data/meesho_reseller.db < part1_sql/queries.sql
```

Save the five required query outputs under:

```text
part1_sql/output/
```

The main Part 1 output consumed by later parts is:

```text
part1_sql/output/monthly_category_revenue.csv
```

## 3. Run Part 2

Copy the Part 1 monthly category CSV into:

```text
part2_engine/fixtures/monthly_category_revenue.csv
```

Then run:

```bash
python part2_engine/test_growth_engine.py
```

Or, if pytest is installed:

```bash
pytest part2_engine/test_growth_engine.py
```

## 4. Run Part 3

Review:

```text
part3_narrative/prompt_pack.md
part3_narrative/narrative_report.md
part3_narrative/masking.py
```

The narrative layer is deterministic and offline; it does not require an LLM API.

## 5. Run Part 4

Create month-specific CSV feeds from the Part 1 output, with the same four columns:

```text
month,category,revenue,n_orders
```

Then run the mock runner:

```bash
python part4_agent/mock_agent_runner.py May <AprilCSV> <MayCSV>
```

The runner validates the current feed, computes MoM changes using Part 2 without reimplementing those functions, ranks flagged categories, drafts at most three messages, suppresses additional flagged categories, records exact-boundary escalations, and holds all drafts for human approval.

## Workflow mapping

- **Part 1 → Part 2:** compute verified business numbers with SQL first, then hand the validated feed to the growth engine.
- **Part 2:** converts the vague idea of "significant change" into deterministic numeric rules and input guardrails.
- **Part 3:** converts verified numbers into a stakeholder narrative while preventing unsupported figures and raw reseller-name leakage.
- **Part 4:** mirrors an Intake → Validate → Compute → Rank → Draft → Human Review workflow with a hard stop on invalid input.

## Official acceptance values

The seeded dataset should produce the values stated in the project brief, including:

- Grand total revenue: INR 1262066.92
- June Delivered AOV: INR 1267.69
- Zero-order reseller: RS024
- May Ethnic Wear MoM: 77.1%
- June Ethnic Wear MoM: -58.74%

## Academic integrity

Implementation uses Python standard-library functionality such as `csv`, `sqlite3`, and `unittest`/assertions. Official Python documentation may be consulted while implementing the project.
