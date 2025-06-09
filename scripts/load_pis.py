# load_pi_devices.py

import json
import os
import sys

import django

# Add the project root (parent of 'config') to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from pi_tracker.models import PiDevice  # noqa E402

fixture_file = "pi_tracker/fixtures/pi_devices.json"

with open(fixture_file, "r") as f:
    data = json.load(f)

for entry in data:
    fields = entry["fields"]
    print("Fields to be processed:", fields)
    print("type(fields):", type(fields))
    for key in fields.keys():
        print("key:", key)
        print("value:", fields[key])
    # obj, created = PiDevice.objects.update_or_create(
    #     name=fields["name"],
    #     defaults=fields,
    # )
    # print(f"{'Created' if created else 'Updated'}: {obj}")
