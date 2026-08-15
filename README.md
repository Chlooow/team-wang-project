# team-wang-project

Minimal ELT scaffold for Team Wang Shopify data using **dlt + dbt + Dagster** with an **Excel output** and **SCD2 historization**.

## What is included

- `team_wang_elt/dlt_shopify.py`: loads Shopify order JSON into DuckDB using dlt.
- `dbt/snapshots/shopify_orders_scd2.sql`: dbt SCD2 snapshot strategy for order historization.
- `team_wang_elt/dagster_defs.py`: Dagster job wiring ingestion -> snapshot -> Excel export.
- `team_wang_elt/excel_export.py`: exports historized table to `output/shopify_orders_scd2.xlsx`.
- `tests/test_scd2.py`: focused tests for SCD2 historization behavior.

## Quick start

1. Install dependencies:
   - `pip install -e .[dev]`
2. Load data and build snapshot through Dagster job:
   - `python -c "from team_wang_elt.dagster_defs import team_wang_elt_job; team_wang_elt_job.execute_in_process()"`
3. Generated Excel output:
   - `output/shopify_orders_scd2.xlsx`

## Notes

- This scaffold uses local sample data in `data/shopify/orders.json`.
- Replace that file or extend `dlt_shopify.py` with authenticated Shopify API calls when credentials are available.
