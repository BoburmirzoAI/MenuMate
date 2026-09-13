from django.db import models

from apps.shared.models import BaseModel


class Permission(BaseModel):
    """
    Base permissions — hierarchic (parent-child) so a group permission
    (e.g. "menu.manage") implies its children ("menu.create", "menu.edit").
    """
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
    )

    class Meta:
        db_table = 'users_permission_custom'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_all_permissions(self):
        perms = [self]
        for child in self.children.all():
            perms.extend(child.get_all_permissions())
        return perms


class Endpoint(BaseModel):
    """Database-backed registry of every API endpoint and who can hit it."""

    HTTP_METHODS = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
    ]
    ACCESS_TYPES = [
        ('public', 'Public'),
        ('authenticated', 'Authenticated'),
        ('permission', 'Permission Required'),
    ]

    path = models.CharField(max_length=255, help_text="e.g. /api/v1/menu/{id}/")
    method = models.CharField(max_length=10, choices=HTTP_METHODS)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    permission = models.ForeignKey(
        Permission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='endpoints',
    )
    access_type = models.CharField(
        max_length=20,
        choices=ACCESS_TYPES,
        default='authenticated',
        db_index=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users_endpoint'
        unique_together = ('path', 'method')
        ordering = ['path', 'method']

    def __str__(self):
        return f"{self.method} {self.path}"

    @classmethod
    def check_access(cls, user, path, method):
        endpoint = cls.objects.filter(
            path=path,
            method=method.upper(),
            is_active=True,
        ).select_related('permission').first()

        if not endpoint:
            return False

        if endpoint.access_type == 'public':
            return True

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if endpoint.access_type == 'authenticated':
            return True

        if endpoint.access_type == 'permission':
            if not endpoint.permission:
                return False
            return user.has_permission(endpoint.permission.codename)

        return False


class Role(BaseModel):
    """Reusable bundle of permissions (admin, family_head, viewer, ...)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, related_name='roles', blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users_role'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_all_permissions(self):
        all_perms = set()
        for perm in self.permissions.all():
            all_perms.update(perm.get_all_permissions())
        return list(all_perms)
