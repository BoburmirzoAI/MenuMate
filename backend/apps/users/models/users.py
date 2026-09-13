"""
Menu Mate — User model (soddalashtirilgan).

Barcha shaxsiy ma'lumot, sozlamalar va tasdiqlash holati shu modelda.
Alohida Profile / Preferences / Verification modellar YO'Q.
"""
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from apps.shared.models import BaseModel, Language


phone_regex = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Telefon raqam +998901234567 formatida bo'lishi kerak",
)


class Gender(models.TextChoices):
    MALE = 'MALE', 'Erkak'
    FEMALE = 'FEMALE', 'Ayol'
    OTHER = 'OTHER', 'Boshqa'


class UserManager(BaseUserManager):
    """Custom manager — email based, soft-delete aware."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def with_deleted(self):
        return super().get_queryset()

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email majburiy")
        email = self.normalize_email(email).lower()

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_email_verified', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser is_staff=True bo'lishi kerak")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser is_superuser=True bo'lishi kerak")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Menu Mate foydalanuvchisi (oila boshlig'i)."""

    # === Auth ===
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(
        max_length=20, validators=[phone_regex],
        unique=True, null=True, blank=True, db_index=True,
    )

    # === Shaxsiy ma'lumot ===
    first_name = models.CharField(max_length=64, blank=True, default='')
    last_name = models.CharField(max_length=64, blank=True, default='')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=Gender.choices, null=True, blank=True,
    )
    avatar = models.ForeignKey(
        'shared.Media',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+',
    )

    # === Sozlamalar ===
    language = models.CharField(
        max_length=5, choices=Language.choices, default=Language.UZ,
    )
    timezone = models.CharField(max_length=64, default='Asia/Tashkent')
    is_push_enabled = models.BooleanField(default=True)

    # === Tasdiqlash ===
    is_email_verified = models.BooleanField(default=False, db_index=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    # === Ruxsatlar ===
    roles = models.ManyToManyField(
        'permissions.Role', related_name='users', blank=True,
    )
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # === Soft delete ===
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # === Onboarding ===
    is_onboarded = models.BooleanField(
        default=False,
        help_text="Oila yaratilganmi",
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users_user'
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['is_deleted', '-created_at']),
        ]

    def __str__(self):
        return self.full_name or self.email

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def short_name(self) -> str:
        return self.first_name or self.email.split('@')[0]

    def has_permission(self, codename: str) -> bool:
        if self.is_superuser:
            return True
        if self.roles.filter(
                is_active=True, permissions__codename=codename,
        ).exists():
            return True
        if self.user_permissions_direct.filter(
                is_active=True, permission__codename=codename,
        ).exists():
            return True
        return False

    def verify_email(self):
        self.is_email_verified = True
        self.email_verified_at = timezone.now()
        self.save(update_fields=['is_email_verified', 'email_verified_at'])

    def soft_delete(self):
        """
        Soft delete — is_deleted=True qilinadi.
        Email va phone anonimizatsiya qilinadi (boshqa foydalanuvchi shu
        email/telefonda register qilishi mumkin bo'lishi uchun).
        Phone_number max_length=20 bo'lgani uchun uni None qilib qo'yamiz
        (prefix qo'shsak overflow bo'ladi).
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.is_active = False
        self.email = f"deleted_{self.id}_{self.email}"[:255]
        self.phone_number = None
        self.save(update_fields=[
            'is_deleted', 'deleted_at', 'is_active', 'email', 'phone_number',
        ])

    def mark_onboarded(self):
        if not self.is_onboarded:
            self.is_onboarded = True
            self.save(update_fields=['is_onboarded'])
