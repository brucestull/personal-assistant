#!/usr/bin/env python3
import json
import argparse
import sys


def renumber_notetags_and_update_notes(input_path, output_path, start_notetag_pk):
    # Load the full fixture list
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Step 1: Renumber notetag entries, build old→new map
    notetag_map = {}
    next_pk = start_notetag_pk
    for entry in data:
        if entry.get("model") == "unimportant_notes.notetag":
            old_pk = entry["pk"]
            notetag_map[old_pk] = next_pk
            entry["pk"] = next_pk
            next_pk += 1

    # Step 2: Update each unimportantnote’s tag references
    updated_tags = 0
    for entry in data:
        if entry.get("model") == "unimportant_notes.unimportantnote":
            tags = entry["fields"].get("tag", [])
            new_tags = []
            for t in tags:
                if t in notetag_map:
                    new_tags.append(notetag_map[t])
                    updated_tags += 1
                else:
                    # leave it untouched if it wasn’t a notetag
                    new_tags.append(t)
            entry["fields"]["tag"] = new_tags

    # Write out the updated fixture
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total_notetags = len(notetag_map)
    print(f"✅ Renumbered {total_notetags} notetag PKs starting at {start_notetag_pk}")
    print(f"✅ Updated {updated_tags} tag references in unimportantnote entries")
    print(f"→ Written updated fixture to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Renumber unimportant_notes.notetag PKs and update unimportantnote.tag references."  # noqa: E501
    )
    parser.add_argument(
        "input_file",
        help="Path to your existing fixture JSON (e.g. mom_activities_with_datetime.json)",  # noqa: E501
    )
    parser.add_argument(
        "output_file", help="Path where the updated fixture should be written"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=100,
        help="Starting PK for notetag entries (default: 100)",
    )
    args = parser.parse_args()

    try:
        renumber_notetags_and_update_notes(
            args.input_file, args.output_file, args.start
        )
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
