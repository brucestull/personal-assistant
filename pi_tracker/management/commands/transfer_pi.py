#!/usr/bin/env python3

from django.core.management.base import BaseCommand
from pi_tracker.models import PiDevice

for device in PiDevice.objects.all():
    print(device)


class Command(BaseCommand):
    help = "Transfers data from SourceModel to TargetModel"

    def handle(self, *args, **kwargs):
        # Example logic to transfer data
        source_data = PiDevice.objects.all()  # Get all SourceModel records
        print(f"Found {source_data.count()} devices to transfer.")
        print("source_data:", source_data)

        # for item in source_data:
        #     # Create a corresponding TargetModel entry
        #     TargetModel.objects.create(
        #         field1=item.field1,
        #         field2=item.field2,
        #         # Add other fields as necessary
        #     )

        self.stdout.write(self.style.SUCCESS("Data transfer completed successfully"))
