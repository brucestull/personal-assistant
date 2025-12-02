#!/usr/bin/env python

"""
Tiny helper script to scale Heroku dynos up or down.

Usage (from Heroku Scheduler or CLI):

    python heroku_scale.py up
    python heroku_scale.py down

Configuration (set as Heroku config vars):

    HEROKU_API_KEY       - your Heroku API key
    HEROKU_APP_NAME      - e.g. "personal-assistant"
    DYNO_PROCESS_TYPES   - comma-separated list, e.g. "web,worker"
    DYNO_QTY_UP          - e.g. "1"
    DYNO_QTY_DOWN        - e.g. "0"
"""

import json
import os
import sys
import urllib.request
from typing import Iterable


HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")

# NEW: support multiple process types, default to just "web"
_raw_process_types = os.environ.get("DYNO_PROCESS_TYPES", "web")
DYNO_PROCESS_TYPES: list[str] = [
    p.strip() for p in _raw_process_types.split(",") if p.strip()
]

DYNO_QTY_UP = int(os.environ.get("DYNO_QTY_UP", "1"))
DYNO_QTY_DOWN = int(os.environ.get("DYNO_QTY_DOWN", "0"))


def scale_process(process_type: str, quantity: int) -> None:
    if not HEROKU_API_KEY or not HEROKU_APP_NAME:
        print("Missing HEROKU_API_KEY or HEROKU_APP_NAME config vars.", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/formation/{process_type}"

    data = json.dumps({"quantity": quantity}).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": f"Bearer {HEROKU_API_KEY}",
    }

    request = urllib.request.Request(url, data=data, headers=headers, method="PATCH")

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
            print(
                f"[heroku_scale] Scaled {process_type!r} dynos to quantity={quantity}. "
                f"Status={response.status}"
            )
            if body:
                print(body)
    except Exception as exc:  # noqa: BLE001
        print(f"[heroku_scale] Error scaling {process_type!r}: {exc}", file=sys.stderr)
        sys.exit(1)


def scale_all(process_types: Iterable[str], quantity: int) -> None:
    if not process_types:
        print("[heroku_scale] No process types specified.", file=sys.stderr)
        sys.exit(1)
    for process_type in process_types:
        scale_process(process_type, quantity)


def main(argv: list[str]) -> None:
    if len(argv) != 2 or argv[1] not in {"up", "down"}:
        print("Usage: python heroku_scale.py [up|down]", file=sys.stderr)
        sys.exit(1)

    direction = argv[1]
    quantity = DYNO_QTY_UP if direction == "up" else DYNO_QTY_DOWN

    print(
        f"[heroku_scale] Direction={direction}, quantity={quantity}, "
        f"process_types={DYNO_PROCESS_TYPES}"
    )
    scale_all(DYNO_PROCESS_TYPES, quantity)


if __name__ == "__main__":
    main(sys.argv)
