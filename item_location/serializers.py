from rest_framework import serializers

from .models import Item, StorageLocation


class StorageLocationSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = StorageLocation
        fields = ["id", "name", "type", "item_count", "created", "updated"]
        read_only_fields = ["id", "created", "updated"]

    def get_item_count(self, obj):
        return obj.items.count()


class ItemSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(
        source="location.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "type",
            "location",
            "location_name",
            "created",
            "updated",
        ]
        read_only_fields = ["id", "created", "updated"]
