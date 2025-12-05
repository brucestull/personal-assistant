# kanban_cabinet/management/commands/load_letter_trays.py

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from kanban_cabinet.models import Location, StockItem


LETTER_TRAY_DATA = [
    {
        "location_name": "Letter Tray 01",
        "location_description": "Tray 01 for 3D-printed letter tiles (C–T).",
        "items": [
            # letter, quantity_on_hand, target_quantity
            ("C", 3, 3),
            ("D", 3, 4),
            ("E", 11, 12),
            ("F", 2, 3),
            ("G", 2, 2),
            ("H", 3, 6),
            ("I", 4, 7),
            ("J", 2, 1),
            ("K", 2, 1),
            ("L", 3, 4),
            ("M", 3, 3),
            ("N", 3, 7),
            ("O", 5, 8),
            ("P", 2, 2),
            ("Q", 2, 1),
            ("R", 3, 6),
            ("S", 5, 6),
            ("T", 7, 9),
        ],
    },
    {
        "location_name": "Letter Tray 02",
        "location_description": "Tray 02 for 3D-printed letter tiles (U–Z).",
        "items": [
            ("U", 2, 3),
            ("V", 2, 1),
            ("W", 2, 3),
            ("X", 2, 1),
            ("Y", 2, 2),
            ("Z", 2, 1),
        ],
    },
]


class Command(BaseCommand):
    help = "Load Letter Tray 01 and 02 stock items (letters C–Z) for a given user."

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-id",
            type=int,
            default=1,
            help="Primary key of the user who owns these items (default: 1).",
        )

    def handle(self, *args, **options):
        user_id = options["user_id"]
        User = get_user_model()

        try:
            owner = User.objects.get(pk=user_id)
        except User.DoesNotExist as exc:
            raise CommandError(f"User with pk={user_id} does not exist.") from exc

        total_created = 0
        total_updated = 0

        for tray in LETTER_TRAY_DATA:
            location_name = tray["location_name"]
            location_description = tray["location_description"]

            location, location_created = Location.objects.get_or_create(
                owner=owner,
                name=location_name,
                defaults={
                    "description": location_description,
                    "is_active": True,
                },
            )

            if location_created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created Location: {location_name}")
                )
            else:
                # Optionally keep description in sync
                if location.description != location_description:
                    location.description = location_description
                    location.save(update_fields=["description"])
                    self.stdout.write(
                        self.style.WARNING(
                            f"Updated description for Location: {location_name}"
                        )
                    )
                else:
                    self.stdout.write(f"Using existing Location: {location_name}")

            created_count = 0
            updated_count = 0

            for letter, qty_on_hand, target_qty in tray["items"]:
                name = f"Letter {letter}"
                description = f"3D-printed letter tile '{letter}'."

                stock_item, created = StockItem.objects.update_or_create(
                    owner=owner,
                    name=name,
                    location=location,
                    defaults={
                        "description": description,
                        "is_physical": True,
                        "unit_name": "Tile(s)",
                        "quantity_on_hand": qty_on_hand,
                        "target_quantity": target_qty,
                        "is_active": True,
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Created StockItem: {stock_item} "
                            f"(on_hand={qty_on_hand}, target={target_qty})"
                        )
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        f"  Updated StockItem: {stock_item} "
                        f"(on_hand={qty_on_hand}, target={target_qty})"
                    )

            total_created += created_count
            total_updated += updated_count

            self.stdout.write(
                self.style.SUCCESS(
                    f"Location '{location_name}': "
                    f"created {created_count}, updated {updated_count} items."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"All trays done. Total created: {total_created}, "
                f"total updated: {total_updated}."
            )
        )
