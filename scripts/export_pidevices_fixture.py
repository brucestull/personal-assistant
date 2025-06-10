#!/usr/bin/env python3
# scripts/export_pidevices_fixture.py

import json
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from pi_tracker.models import PiDevice  # noqa: E402

output_file = "pi_tracker/fixtures/pi_devices.json"

fixture = []

for device in PiDevice.objects.all():
    fixture.append(
        {
            "model": "pi_tracker.pidevice",
            "fields": {
                "pk": device.pk,
                "name": device.name,
                "description": device.description,
                "operating_system": device.operating_system,
                "host_name": device.host_name,
                "mac_address": device.mac_address,
                "ram": device.ram,
                "form_factor": device.form_factor,
            },
        }
    )

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write to file
with open(output_file, "w") as f:
    json.dump(fixture, f, indent=2)

print(f"Exported {len(fixture)} PiDevice objects to {output_file}")
