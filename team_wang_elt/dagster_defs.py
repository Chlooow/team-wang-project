from __future__ import annotations

from dagster import Definitions, job, op

from .dbt_runner import run_dbt_snapshot
from .dlt_shopify import run_dlt_load
from .excel_export import export_scd2_to_excel


@op
def ingest_shopify_data() -> dict:
    return run_dlt_load()


@op
def run_historization(_: dict) -> str:
    run_dbt_snapshot()
    return "dbt snapshot complete"


@op
def export_excel(_: str) -> str:
    return export_scd2_to_excel()


@job
def team_wang_elt_job():
    export_excel(run_historization(ingest_shopify_data()))


defs = Definitions(jobs=[team_wang_elt_job])
