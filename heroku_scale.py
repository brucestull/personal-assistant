#!/usr/bin/env python
"""
Tiny helper script to scale Heroku dynos up or down.

Usage (from Heroku Scheduler or CLI):

    python heroku_scale.py up
    python heroku_scale.py down

Configuration (set as Heroku config vars):

    HEROKU_API_KEY      - your Heroku API key
    HEROKU_APP_NAME     - e.g. "personal-assistant"
    DYNO_PROCESS_TYPE   - usually "web"
    DYNO_QTY_UP         - e.g. "1"
    DYNO_QTY_DOWN       - e.g. "0"
"""

import os
import sys
import json
import urllib.request


HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
DYNO_PROCESS_TYPE = os.environ.get("DYNO_PROCESS_TYPE", "web")

DYNO_QTY_UP = int(os.environ.get("DYNO_QTY_UP", "1"))
DYNO_QTY_DOWN = int(os.environ.get("DYNO_QTY_DOWN", "0"))


def scale_dynos(quantity: int) -> None:
    if not HEROKU_API_KEY or not HEROKU_APP_NAME:
        print("Missing HEROKU_API_KEY or HEROKU_APP_NAME config vars.", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/formation/{DYNO_PROCESS_TYPE}"

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
            print(f"Scaled {DYNO_PROCESS_TYPE} dynos to quantity={quantity}.")
            print(f"Heroku response status: {response.status}")
            if body:
                print(body)
    except Exception as exc:  # noqa: BLE001 (this is a tiny ops script)
        print(f"Error talking to Heroku API: {exc}", file=sys.stderr)
        sys.exit(1)


def main(argv: list[str]) -> None:
    if len(argv) != 2 or argv[1] not in {"up", "down"}:
        print("Usage: python heroku_scale.py [up|down]", file=sys.stderr)
        sys.exit(1)

    direction = argv[1]
    quantity = DYNO_QTY_UP if direction == "up" else DYNO_QTY_DOWN
    scale_dynos(quantity)


if __name__ == "__main__":
    main(sys.argv)
