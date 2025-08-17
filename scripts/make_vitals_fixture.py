#!/usr/bin/env python3
"""
Generate a plain JSON fixture for the vitals app.

- 1 user (pk=1, username=testuser)
- 51 BloodPressure
- 20 Pulse
- 20 Temperature
- 20 BodyWeight

Usage (from project root):
    python scripts/make_vitals_fixture.py
Then load:
    python manage.py loaddata vitals_fixture.json
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

# import os

load_dotenv(".env")  # take environment variables from .env

# ── CONFIG ────────────────────────────────────────────────────────────────────
APP_LABEL = "vitals"  # your Django app name containing the models
USER_MODEL = "accounts.CustomUser"  # change to e.g. "accounts.user" if custom user
USER_PK = 1  # pk referenced by fixtures
OUTPUT_NAME = "vitals_fixture.json"

COUNT_BP = 51
COUNT_PULSE = 20
COUNT_TEMP = 20
COUNT_WEIGHT = 20

START_TS = datetime(2025, 1, 1, 12, 0, 0)  # base timestamp
# ──────────────────────────────────────────────────────────────────────────────


def main() -> None:
    # Resolve: scripts/ -> project root -> vitals/fixtures/vitals_fixture.json
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    fixtures_dir = project_root / APP_LABEL / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    out_path = fixtures_dir / OUTPUT_NAME

    records = []

    # --- User ---
    # records.append(
    #     {
    #         "model": USER_MODEL,
    #         "pk": USER_PK,
    #         "fields": {
    #             "username": os.getenv("DJANGO_SU_NAME", "testuser"),
    #             "email": os.getenv("DJANGO_SU_EMAIL", "test@example.com"),
    #             # NOTE: this is a dummy hash, change password later via changepassword
    #             "password": "pbkdf2_sha256$260000$dummy$abcdefghijklmnopqrstuv==",
    #         },
    #     }
    # )

    # --- BloodPressure (51) ---
    for i in range(1, COUNT_BP + 1):
        ts = (START_TS + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        records.append(
            {
                "model": f"{APP_LABEL}.bloodpressure",
                "pk": i,
                "fields": {
                    "user": USER_PK,
                    "systolic": 100 + (i % 40),  # 101..139 repeating-ish
                    "diastolic": 60 + (i % 20),  # 61..79 repeating-ish
                    "pulse": 60 + (i % 40),  # 61..99 repeating-ish
                    "created": ts,
                    "updated": ts,
                },
            }
        )

    # --- Pulse (20) ---
    for i in range(1, COUNT_PULSE + 1):
        ts = (START_TS + timedelta(days=1, hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        records.append(
            {
                "model": f"{APP_LABEL}.pulse",
                "pk": 1000 + i,
                "fields": {
                    "user": USER_PK,
                    "bpm": 60 + (i % 50),  # 61..109 repeating-ish
                    "created": ts,
                    "updated": ts,
                },
            }
        )

    # --- Temperature (20) ---
    for i in range(1, COUNT_TEMP + 1):
        ts = (START_TS + timedelta(days=2, hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        # Use strings for Decimal fields in fixtures (safe across DBs)
        measurement = f"{97.0 + (i % 5):.1f}"  # 97.1..101.0 repeating-ish
        records.append(
            {
                "model": f"{APP_LABEL}.temperature",
                "pk": 2000 + i,
                "fields": {
                    "subject": USER_PK,
                    "measurement": measurement,
                    "created": ts,
                    "updated": ts,
                },
            }
        )

    # --- BodyWeight (20) ---
    for i in range(1, COUNT_WEIGHT + 1):
        ts = (START_TS + timedelta(days=3, hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        weight = f"{150.0 + (i % 30):.2f}"  # 151.00..179.00 repeating-ish
        records.append(
            {
                "model": f"{APP_LABEL}.bodyweight",
                "pk": 3000 + i,
                "fields": {
                    "subject": USER_PK,
                    "measurement": weight,
                    "created": ts,
                    "updated": ts,
                },
            }
        )

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    print(f"Wrote {out_path} with {len(records)} records.")


if __name__ == "__main__":
    main()
