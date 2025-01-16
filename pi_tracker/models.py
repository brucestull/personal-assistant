from django.db import models


class PiDevice(models.Model):
    FORM_FACTOR_CHOICES = [
        ('Pi4', 'Raspberry Pi 4'),
        ('Pi5', 'Raspberry Pi 5'),
        ('PiZero', 'Raspberry Pi Zero'),
        ('PiPico', 'Raspberry Pi Pico'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    operating_system = models.CharField(max_length=100)
    host_name = models.CharField(max_length=100, unique=True)
    mac_address = models.CharField(
        max_length=17, unique=True, help_text="Format: XX:XX:XX:XX:XX:XX")
    ram = models.CharField(max_length=50, help_text="e.g., 2GB, 4GB, 8GB")
    form_factor = models.CharField(max_length=10, choices=FORM_FACTOR_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.host_name})"

    class Meta:
        verbose_name = "Pi Device"
        verbose_name_plural = "Pi Devices"
        ordering = ("name",)
