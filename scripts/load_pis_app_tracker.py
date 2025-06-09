#!/usr/bin/env python3
# scripts/load_pis_app_tracker.py

import json
import os
import sys

import django

# Add the project root (parent of 'config') to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app_tracker.models import Server, OperatingSystem  # noqa E402

fixture_file = "pi_tracker/fixtures/pi_devices.json"


with open(fixture_file, "r") as f:
    data = json.load(f)


for entry in data:
    fields = entry["fields"]
    print("Fields to be processed:", fields)
    # print("type(fields):", type(fields))
    # for key in fields.keys():
    #     print("key:", key)
    #     print("value:", fields[key])
    operating_system = OperatingSystem.objects.get_or_create(
        name=fields["operating_system"]
    )[0]

    obj, created = Server.objects.update_or_create(
        name=fields["name"],
        description=fields.get("description", ""),
        operating_system=operating_system,
        host_name=fields["host_name"],
        mac_address=fields.get("mac_address", ""),
        ram=fields.get("ram", ""),
        form_factor=fields.get("form_factor", ""),
    )
    print(f"{'Created' if created else 'Updated'}: {obj}")
