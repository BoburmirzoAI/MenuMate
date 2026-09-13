from django.db import models

from apps.shared.models import BaseModel, DeviceType


def version_to_code(version: str) -> int:
    """
    "1.2.3" → 10203  — used for numeric comparison in DB queries.
    Supports up to 99.99.99. Non-numeric segments become 0.
    """
    parts = (version or '0.0.0').split('.')
    while len(parts) < 3:
        parts.append('0')
    try:
        major, minor, patch = (int(p) for p in parts[:3])
    except ValueError:
        return 0
    return major * 10000 + minor * 100 + patch


class AppVersion(BaseModel):
    """
    Every mobile app release logged for analytics and history.
    """
    platform = models.CharField(
        max_length=10, choices=DeviceType.choices, db_index=True
    )
    version_number = models.CharField(
        max_length=20, help_text="1.2.3 shaklida"
    )
    version_code = models.PositiveIntegerField(
        db_index=True,
        help_text="version_number'dan avtomatik hisoblanadi (masalan 1.2.3 → 10203)",
    )
    release_date = models.DateField(null=True, blank=True)
    changelog_uz = models.TextField(blank=True)
    changelog_ru = models.TextField(blank=True)
    changelog_en = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users_app_version'
        unique_together = ('platform', 'version_number')
        ordering = ['-version_code']
        indexes = [
            models.Index(fields=['platform', '-version_code']),
        ]

    def save(self, *args, **kwargs):
        self.version_code = version_to_code(self.version_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.platform} {self.version_number}"


class VersionPolicy(BaseModel):
    """
    Har bir platform (iOS, Android) uchun bitta qator:
    - current_version — App Store / Play Store'dagi eng oxirgi versiya
    - min_required_version — bundan past versiyalar UPDATE_REQUIRED oladi
    - min_os_version — qurilmaning OS versiyasi bundan past bo'lsa UPDATE_REQUIRED

    Admin panelidan boshqariladi.
    """
    platform = models.CharField(
        max_length=10, choices=DeviceType.choices, unique=True
    )
    current_version = models.CharField(max_length=20, help_text="1.2.3")
    min_required_version = models.CharField(
        max_length=20,
        help_text="Bundan past versiyalar force update qilinadi (masalan 1.0.0)",
    )
    min_os_version = models.CharField(
        max_length=20, blank=True,
        help_text="Masalan iOS: '13.0', Android: '8.0'. Bo'sh bo'lsa OS tekshirilmaydi",
    )
    store_url = models.URLField(
        blank=True,
        help_text="App Store yoki Play Store havolasi (update tugmasi uchun)",
    )
    message_uz = models.TextField(
        blank=True,
        help_text="Foydalanuvchiga ko'rsatiladigan xabar",
    )
    message_ru = models.TextField(blank=True)
    message_en = models.TextField(blank=True)

    class Meta:
        db_table = 'users_version_policy'
        verbose_name = 'Version policy'
        verbose_name_plural = 'Version policies'

    def __str__(self):
        return f"{self.platform}: current={self.current_version}, min={self.min_required_version}"

    def check_version(self, client_version: str, os_version: str = '') -> dict:
        """
        Returns:
            {
                'status': 'OK' | 'UPDATE_RECOMMENDED' | 'UPDATE_REQUIRED',
                'reason': 'app_outdated' | 'os_outdated' | None,
                'current_version': '1.5.0',
                'min_required_version': '1.2.0',
                'store_url': '...',
                'message': '...',
            }
        """
        client_code = version_to_code(client_version)
        min_code = version_to_code(self.min_required_version)
        latest_code = version_to_code(self.current_version)

        # OS check first — hardware limit is strictest
        if self.min_os_version and os_version:
            if version_to_code(os_version) < version_to_code(self.min_os_version):
                return {
                    'status': 'UPDATE_REQUIRED',
                    'reason': 'os_outdated',
                    'current_version': self.current_version,
                    'min_required_version': self.min_required_version,
                    'min_os_version': self.min_os_version,
                    'store_url': self.store_url,
                }

        if client_code < min_code:
            return {
                'status': 'UPDATE_REQUIRED',
                'reason': 'app_outdated',
                'current_version': self.current_version,
                'min_required_version': self.min_required_version,
                'store_url': self.store_url,
            }

        if client_code < latest_code:
            return {
                'status': 'UPDATE_RECOMMENDED',
                'reason': None,
                'current_version': self.current_version,
                'min_required_version': self.min_required_version,
                'store_url': self.store_url,
            }

        return {
            'status': 'OK',
            'reason': None,
            'current_version': self.current_version,
            'min_required_version': self.min_required_version,
        }
