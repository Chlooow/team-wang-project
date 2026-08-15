from datetime import datetime

from team_wang_elt.scd2 import historize_scd2


def test_historize_scd2_closes_previous_version_when_values_change():
    rows = [
        {
            "id": 1,
            "email": "a@example.com",
            "financial_status": "pending",
            "loaded_at": datetime.fromisoformat("2026-08-10T10:00:00"),
        },
        {
            "id": 1,
            "email": "a@example.com",
            "financial_status": "paid",
            "loaded_at": datetime.fromisoformat("2026-08-11T10:00:00"),
        },
    ]

    result = historize_scd2(rows, business_key="id", tracked_fields=["email", "financial_status"])

    assert len(result) == 2
    assert result[0]["is_current"] is False
    assert result[0]["valid_to"] == datetime.fromisoformat("2026-08-11T10:00:00")
    assert result[1]["is_current"] is True
    assert result[1]["valid_to"] is None


def test_historize_scd2_ignores_unchanged_versions():
    rows = [
        {
            "id": 2,
            "email": "b@example.com",
            "financial_status": "pending",
            "loaded_at": datetime.fromisoformat("2026-08-10T10:00:00"),
        },
        {
            "id": 2,
            "email": "b@example.com",
            "financial_status": "pending",
            "loaded_at": datetime.fromisoformat("2026-08-11T10:00:00"),
        },
    ]

    result = historize_scd2(rows, business_key="id", tracked_fields=["email", "financial_status"])

    assert len(result) == 1
    assert result[0]["is_current"] is True
