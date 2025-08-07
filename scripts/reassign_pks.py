#!/usr/bin/env python3
import argparse
import json
import sys


def reassign_pks(django_model, input_path, output_path, start_pk):
    # Load the full fixture list
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Reassign PKs on all 'django_model' entries
    current = start_pk
    for entry in data:
        if entry.get("model") == django_model:
            entry["pk"] = current
            current += 1

    # Write out the updated fixture
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    count = current - start_pk
    print(
        f"✅ Reassigned {count} '{django_model}' PKs starting at {start_pk} and wrote to {output_path}"  # noqa: E501
    )


def main():
    parser = argparse.ArgumentParser(
        description="Reassign PKs for model entries in a Django fixture."  # noqa: E501
    )
    parser.add_argument(
        "django_model",
        help="The model to reassign PKs for (e.g. unimportant_notes.unimportantnote)",  # noqa: E501
    )
    parser.add_argument(
        "input_file",
        help="Path to your existing fixture JSON (e.g. activities_with_datetime.json)",  # noqa: E501
    )
    parser.add_argument(
        "output_file", help="Path where the updated fixture should be written"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=620,
        help="Starting PK value for the first unimportantnote (default: 620)",
    )
    args = parser.parse_args()

    try:
        reassign_pks(args.django_model, args.input_file, args.output_file, args.start)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
