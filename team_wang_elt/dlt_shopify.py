from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import dlt


def _read_orders(json_path: Path) -> list[dict[str, Any]]:
    with json_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return payload if isinstance(payload, list) else payload.get("orders", [])


@dlt.resource(name="shopify_orders", write_disposition="append", primary_key="id")
def shopify_orders_resource(records: list[dict[str, Any]]):
    yield from records


def run_dlt_load(
    json_path: str = "data/shopify/orders.json",
    duckdb_path: str = ".duckdb/team_wang.duckdb",
) -> dict[str, Any]:
    records = _read_orders(Path(json_path))
    pipeline = dlt.pipeline(
        pipeline_name="team_wang_shopify",
        destination=dlt.destinations.duckdb(duckdb_path),
        dataset_name="raw_shopify",
    )
    load_info = pipeline.run(shopify_orders_resource(records))
    return {
        "loaded_rows": len(records),
        "pipeline": "team_wang_shopify",
        "load_info": str(load_info),
        "duckdb_path": duckdb_path,
    }
