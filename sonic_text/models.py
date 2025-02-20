from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AudioFile(models.Model):
    """
    Model for audio files.
    Attributes:
        name (str): The name of the audio file.
        description (str): A description of the audio file.
        file (FileField): The audio file itself.
        file_type (str): The type of the audio file.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="sonic_audio_files/")
    file_type = models.CharField(max_length=10, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audio_files")

    def save(self, *args, **kwargs):
        if self.file:
            self.file_type = self.file.name.split(".")[-1].lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("sonic_text:audiofile_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Audio File"
        verbose_name_plural = "Audio Files"
