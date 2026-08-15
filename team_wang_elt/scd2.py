from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from hashlib import sha256
from typing import Any


def _version_hash(record: dict[str, Any], tracked_fields: list[str]) -> str:
    joined = "|".join(str(record.get(field, "")) for field in tracked_fields)
    return sha256(joined.encode("utf-8")).hexdigest()


def historize_scd2(
    records: Iterable[dict[str, Any]],
    business_key: str,
    tracked_fields: list[str],
    loaded_at_field: str = "loaded_at",
) -> list[dict[str, Any]]:
    """Build SCD2 rows from Shopify-style snapshots.

    Input rows are expected to contain one business key and load timestamp.
    Rows with unchanged tracked fields are ignored.
    """
    sorted_records = sorted(records, key=lambda r: (r[business_key], r[loaded_at_field]))
    output: list[dict[str, Any]] = []
    current_by_key: dict[str, dict[str, Any]] = {}

    for row in sorted_records:
        key = str(row[business_key])
        loaded_at = row[loaded_at_field]
        if isinstance(loaded_at, str):
            loaded_at = datetime.fromisoformat(loaded_at)

        row_hash = _version_hash(row, tracked_fields)
        existing = current_by_key.get(key)

        if existing and existing["scd2_hash"] == row_hash:
            continue

        if existing:
            existing["valid_to"] = loaded_at
            existing["is_current"] = False

        version = dict(row)
        version["valid_from"] = loaded_at
        version["valid_to"] = None
        version["is_current"] = True
        version["scd2_hash"] = row_hash
        output.append(version)
        current_by_key[key] = version

    return output
