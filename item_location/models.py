from django.conf import settings
from django.db import models
from django.urls import reverse

from base.models import CreatedUpdatedBase


LOCATION_TYPE_CHOICES = [
    ("room", "Room"),
    ("cabinet", "Cabinet"),
    ("shelf", "Shelf"),
    ("drawer", "Drawer"),
    ("box", "Box"),
    ("bin", "Bin"),
    ("closet", "Closet"),
    ("garage", "Garage"),
    ("attic", "Attic"),
    ("basement", "Basement"),
    ("other", "Other"),
]

ITEM_TYPE_CHOICES = [
    ("tool", "Tool"),
    ("clothing", "Clothing"),
    ("electronics", "Electronics"),
    ("document", "Document"),
    ("food", "Food"),
    ("book", "Book"),
    ("toy", "Toy"),
    ("sports", "Sports Equipment"),
    ("kitchen", "Kitchen Item"),
    ("furniture", "Furniture"),
    ("other", "Other"),
]


class StorageLocation(CreatedUpdatedBase):
    """
    A named storage location (e.g. a shelf, cabinet, drawer) owned by a user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="storage_locations",
        verbose_name="User",
    )
    name = models.CharField(
        "Name",
        max_length=255,
        help_text="Name of the storage location.",
    )
    type = models.CharField(
        "Type",
        max_length=100,
        choices=LOCATION_TYPE_CHOICES,
        default="other",
        help_text="Type of storage location.",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Storage Location"
        verbose_name_plural = "Storage Locations"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def get_absolute_url(self):
        return reverse("item_location:location-detail", kwargs={"pk": self.pk})


class Item(CreatedUpdatedBase):
    """
    An item that may be stored in a StorageLocation, owned by a user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stored_items",
        verbose_name="User",
    )
    name = models.CharField(
        "Name",
        max_length=255,
        help_text="Name of the item.",
    )
    type = models.CharField(
        "Type",
        max_length=100,
        choices=ITEM_TYPE_CHOICES,
        default="other",
        help_text="Type of item.",
    )
    location = models.ForeignKey(
        StorageLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
        verbose_name="Storage Location",
        help_text="Where this item is stored.",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        if self.location:
            return f"{self.name} ({self.get_type_display()}) @ {self.location.name}"
        return f"{self.name} ({self.get_type_display()})"

    def get_absolute_url(self):
        return reverse("item_location:item-detail", kwargs={"pk": self.pk})
