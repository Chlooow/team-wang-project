from __future__ import annotations

from pathlib import Path

import duckdb


def export_scd2_to_excel(
    duckdb_path: str = ".duckdb/team_wang.duckdb",
    table_name: str = "shopify_orders_scd2",
    output_path: str = "output/shopify_orders_scd2.xlsx",
) -> str:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    query = f"SELECT * FROM {table_name} ORDER BY id, valid_from"
    with duckdb.connect(duckdb_path) as conn:
        frame = conn.execute(query).fetch_df()
    frame.to_excel(output, index=False)
    return str(output)
