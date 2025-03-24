import json
from uc_goals.models import VIACharacterStrength

# Load the VIA Character Strengths from the JSON file
with open("uc_goals/dicts/via_character_strengths.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Loop through the data and create a VIACharacterStrength object for each entry
for entry in data:
    obj, created = VIACharacterStrength.objects.update_or_create(
        name=entry["name"],
        defaults={
            "description": entry["description"],
        },
    )
    if created:
        print(f"Created {obj.name}")
    else:
        print(f"Updated {obj.name}")
