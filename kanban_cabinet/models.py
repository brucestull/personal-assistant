# kanban_cabinet/models.py

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Location(models.Model):
    """
    A physical or logical place where items live.
    For example: "Bathroom Cabinet / Top Shelf / Left Bin" or "Digital Licenses".
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kanban_locations",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("owner", "name")
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self) -> str:
        return self.name


class StockItem(models.Model):
    """
    An item you want to track KANBAN‑cabinet style.
    Can be physical (screws, shampoo) or virtual (licenses, S3 buckets).
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kanban_items",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="items",
        null=True,
        blank=True,
        help_text="Where this item normally lives.",
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    is_physical = models.BooleanField(
        default=True,
        help_text="Uncheck if this is a purely digital / virtual item.",
    )
    unit_name = models.CharField(
        max_length=50,
        default="unit",
        help_text="Example: pill, ml, screw, roll, license, bucket",
    )
    quantity_on_hand = models.PositiveIntegerField(default=0)
    target_quantity = models.PositiveIntegerField(
        default=0,
        help_text="How many you like to keep on hand when fully stocked.",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("owner", "name", "location")
        verbose_name = "Stock Item"
        verbose_name_plural = "Stock Items"

    def __str__(self) -> str:
        if self.location:
            return f"{self.name} @ {self.location}"
        return self.name

    @property
    def quantity_to_restock(self) -> int:
        """
        How many you need to acquire to reach the target quantity.
        Never returns a negative number.
        """
        diff = int(self.target_quantity) - int(self.quantity_on_hand)
        return diff if diff > 0 else 0

    @property
    def needs_restock(self) -> bool:
        return self.quantity_to_restock > 0

    def save(self, *args, **kwargs):
        """
        Auto-generate slug from name if not set.
        Handle collisions by appending -2, -3, etc.
        """
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 2
            while StockItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
