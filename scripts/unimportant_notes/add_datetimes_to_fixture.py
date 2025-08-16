#! /usr/bin/env python3

import json
from datetime import datetime, timezone

# File paths
input_path = "unimportant_notes/fixtures/mom_activities.json"
output_path = "unimportant_notes/fixtures/mom_activities_with_datetime.json"

model_app_and_name = "unimportant_notes.unimportantnote"

# Load the JSON fixture
with open(input_path, "r", encoding="utf-8") as infile:
    data = json.load(infile)

# Current UTC timestamp in Django-compatible format
now = datetime.now(timezone.utc).isoformat()

# Inject timestamps for each unimportant note
for obj in data:
    if obj["model"] == model_app_and_name:
        obj["fields"]["created"] = now
        obj["fields"]["updated"] = now

# Save the modified data
with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, indent=2, ensure_ascii=False)

print(f"Updated fixture written to: {output_path}")
