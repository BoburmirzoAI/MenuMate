import os
import uuid

from django.db import models
from django.utils import timezone


class Language(models.TextChoices):
    UZ = "UZ", "Uzbek"
    RU = "RU", "Russian"
    EN = "EN", "English"


class DeviceType(models.TextChoices):
    IOS = "IOS", "iOS"
    ANDROID = "ANDROID", "Android"
    WEB = "WEB", "Web"


class BaseModel(models.Model):
    """
    Abstract base model with UUID and timestamp fields.
    All app models should inherit from this.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


def media_upload_path(instance, filename):
    """uploads/<file_type>/YYYY/MM/<uuid>_<filename>"""
    now = timezone.now()
    ext = os.path.splitext(filename)[1]
    unique_name = f"{instance.uuid}{ext}"
    return f"uploads/{instance.file_type.lower()}/{now.year}/{now.month:02d}/{unique_name}"


class Media(BaseModel):
    """Reusable media model — any app can ForeignKey to it."""

    class FileType(models.TextChoices):
        IMAGE = 'IMAGE', 'Image'
        VIDEO = 'VIDEO', 'Video'
        DOCUMENT = 'DOCUMENT', 'Document'
        OTHER = 'OTHER', 'Other'

    file = models.FileField(upload_to=media_upload_path)
    file_type = models.CharField(
        max_length=20, choices=FileType.choices, default=FileType.IMAGE
    )
    original_name = models.CharField(max_length=255, blank=True)
    size = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = 'shared_media'

    def __str__(self):
        return f"{self.file_type}: {self.original_name or self.uuid}"
