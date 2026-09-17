"""
Default Permission/Role va admin endpoint sozlamalarini yaratuvchi data migration.

Idempotent — mavjud yozuvlarni buzmaydi:
- Permission/Role — get_or_create bilan, faqat yo'q bo'lganda yaratiladi.
- Default rollar (Super Admin, Admin, Moderator, User) — permissions M2M
  yangi rol yaratilganda yoki M2M bo'sh bo'lganda to'ldiriladi. Admin qo'lda
  o'zgartirgan rollar tegilmay qoladi.
- Admin endpointlari — faqat `access_type='authenticated'` bo'lganlari
  `permission`ga o'tkaziladi. Admin qo'lda `permission` yoki `public`
  qilib qo'yganlari saqlanadi.
- Mavjud is_superuser foydalanuvchilarga Super Admin, is_staff (superuser
  emas) foydalanuvchilarga Admin roli beriladi — faqat ular hech qanday
  rolga ega bo'lmasa.
"""
import re

from django.db import migrations


PERMISSIONS: list[tuple[str, str, str, str | None]] = [
    ('dashboard.view',           'Dashboard ko\'rish',            'Admin panel bosh sahifasi', None),
    ('stats.view',               'Statistika ko\'rish',           'KPI va tizim ko\'rsatkichlari', None),

    ('users.manage',             'Foydalanuvchilarni boshqarish', 'Foydalanuvchilar ustidan to\'liq nazorat', None),
    ('users.view',               'Foydalanuvchilarni ko\'rish',   'Ro\'yxat va profil', 'users.manage'),
    ('users.create',             'Foydalanuvchi yaratish',        'Yangi foydalanuvchi qo\'shish', 'users.manage'),
    ('users.edit',               'Foydalanuvchi tahrirlash',      'Profil, rol va parolni yangilash', 'users.manage'),
    ('users.delete',             'Foydalanuvchi o\'chirish',      'Soft-delete', 'users.manage'),

    ('families.manage',          'Oilalarni boshqarish',          'Oila profillari va a\'zolar', None),
    ('families.view',            'Oilalarni ko\'rish',            'Ro\'yxat va tafsilotlar', 'families.manage'),
    ('families.edit',            'Oila tahrirlash',               'Nomi, shahar, a\'zolar', 'families.manage'),
    ('families.delete',          'Oila o\'chirish',               'Oilani o\'chirish', 'families.manage'),

    ('recipes.manage',           'Retseptlarni boshqarish',       'To\'liq nazorat', None),
    ('recipes.view',             'Retseptlarni ko\'rish',         'Ro\'yxat', 'recipes.manage'),
    ('recipes.create',           'Retsept yaratish',              'Yangi retsept', 'recipes.manage'),
    ('recipes.edit',             'Retsept tahrirlash',            'Yangilash', 'recipes.manage'),
    ('recipes.delete',           'Retsept o\'chirish',            'O\'chirish', 'recipes.manage'),

    ('ingredients.manage',       'Ingredientlarni boshqarish',    'Katalog nazorati', None),
    ('ingredients.view',         'Ingredientlarni ko\'rish',      'Ro\'yxat', 'ingredients.manage'),
    ('ingredients.create',       'Ingredient yaratish',           'Yangi ingredient', 'ingredients.manage'),
    ('ingredients.edit',         'Ingredient tahrirlash',         'Yangilash', 'ingredients.manage'),
    ('ingredients.delete',       'Ingredient o\'chirish',         'O\'chirish', 'ingredients.manage'),

    ('menus.manage',             'Menyularni boshqarish',         'Menyularni kuzatish va o\'chirish', None),
    ('menus.view',               'Menyularni ko\'rish',           'Ro\'yxat', 'menus.manage'),
    ('menus.delete',             'Menyu o\'chirish',              'O\'chirish', 'menus.manage'),

    ('notifications.manage',     'Bildirishnomalarni boshqarish', 'Push va broadcast', None),
    ('notifications.view',       'Bildirishnomalarni ko\'rish',   'Push tarixi', 'notifications.manage'),
    ('notifications.broadcast',  'Bildirishnoma yuborish',        'Ommaviy push', 'notifications.manage'),

    ('holidays.manage',          'Bayramlarni boshqarish',        'Barcha bayramlar', None),
    ('holidays.view',            'Bayramlarni ko\'rish',          'Ro\'yxat', 'holidays.manage'),
    ('holidays.create',          'Bayram yaratish',               'Yangi bayram', 'holidays.manage'),
    ('holidays.edit',            'Bayram tahrirlash',             'Yangilash', 'holidays.manage'),
    ('holidays.delete',          'Bayram o\'chirish',             'O\'chirish', 'holidays.manage'),

    ('devices.view',             'Qurilmalarni ko\'rish',         'FCM token holati', None),

    ('weather.manage',           'Ob-havoni boshqarish',          'Cache holati', None),
    ('weather.view',             'Ob-havo cache ko\'rish',        'Snapshot yozuvlari', 'weather.manage'),
    ('weather.clear',            'Ob-havo cache tozalash',        'Cache\'ni bo\'shatish', 'weather.manage'),

    ('permissions.manage',       'Ruxsat tizimini boshqarish',    'RBAC nazorati', None),
    ('permissions.view',         'Ruxsatlarni ko\'rish',          'Rollar/permissionlar/endpointlar', 'permissions.manage'),
    ('permissions.edit_role',    'Rolni tahrirlash',              'Yaratish/o\'chirish/tuzatish', 'permissions.manage'),
    ('permissions.edit_permission', 'Permissionni tahrirlash',    'Yaratish/tuzatish', 'permissions.manage'),
    ('permissions.edit_endpoint',   'Endpointni sozlash',         'access_type\'ni o\'zgartirish', 'permissions.manage'),
]

ROLES: list[tuple[str, str, list[str] | None]] = [
    ('Super Admin', 'Barcha huquqlar. RBAC boshqaruvi bilan.', None),
    ('Admin',       'Kontent va foydalanuvchi boshqaruvi.', [
        'dashboard.view', 'stats.view',
        'users.manage', 'families.manage',
        'recipes.manage', 'ingredients.manage',
        'menus.manage', 'notifications.manage',
        'holidays.manage', 'devices.view', 'weather.manage',
        'permissions.view',
    ]),
    ('Moderator', 'Kontent boshqaruvi — retseptlar va bayramlar.', [
        'dashboard.view', 'stats.view',
        'recipes.manage', 'ingredients.manage',
        'holidays.manage', 'notifications.broadcast',
    ]),
    ('User', 'Oddiy foydalanuvchi — admin panelga kirmaydi.', []),
]


def _endpoint_permission_for(path: str, method: str) -> str | None:
    if not path.startswith('/api/v1/admin/'):
        return None
    p = path[len('/api/v1/admin/'):]
    ORDER: list[tuple[str, dict[str, str] | str]] = [
        ('stats/',                                 'stats.view'),
        ('users/{id}/password/',                   'users.edit'),
        ('users/{id}/',                            {'GET': 'users.view', 'PATCH': 'users.edit', 'DELETE': 'users.delete'}),
        ('users/',                                 {'GET': 'users.view', 'POST': 'users.create'}),
        ('families/{id}/members/{id}/',            {'GET': 'families.view', 'PATCH': 'families.edit', 'DELETE': 'families.edit'}),
        ('families/{id}/members/',                 {'GET': 'families.view', 'POST': 'families.edit'}),
        ('families/{id}/',                         {'GET': 'families.view', 'PATCH': 'families.edit', 'DELETE': 'families.delete'}),
        ('families/',                              {'GET': 'families.view', 'POST': 'families.edit'}),
        ('recipes/ingredients/{id}/',              {'GET': 'ingredients.view', 'PATCH': 'ingredients.edit', 'DELETE': 'ingredients.delete'}),
        ('recipes/ingredients/',                   {'GET': 'ingredients.view', 'POST': 'ingredients.create'}),
        ('recipes/allergens/{id}/',                'recipes.edit'),
        ('recipes/allergens/',                     'recipes.edit'),
        ('recipes/{id}/',                          {'GET': 'recipes.view', 'PATCH': 'recipes.edit', 'DELETE': 'recipes.delete'}),
        ('recipes/',                               {'GET': 'recipes.view', 'POST': 'recipes.create'}),
        ('menus/{id}/',                            {'GET': 'menus.view', 'DELETE': 'menus.delete'}),
        ('menus/',                                 'menus.view'),
        ('shopping/by-menu/{id}/',                 'menus.view'),
        ('shopping/',                              'menus.view'),
        ('notifications/holidays/{id}/',           {'GET': 'holidays.view', 'PATCH': 'holidays.edit', 'DELETE': 'holidays.delete'}),
        ('notifications/holidays/',                {'GET': 'holidays.view', 'POST': 'holidays.create'}),
        ('notifications/broadcast/',               'notifications.broadcast'),
        ('notifications/',                         'notifications.view'),
        ('devices/',                               'devices.view'),
        ('weather/',                               {'GET': 'weather.view', 'DELETE': 'weather.clear'}),
        ('permissions/roles/{id}/',                {'GET': 'permissions.view', 'PATCH': 'permissions.edit_role', 'DELETE': 'permissions.edit_role'}),
        ('permissions/roles/',                     {'GET': 'permissions.view', 'POST': 'permissions.edit_role'}),
        ('permissions/permissions/{id}/',          {'GET': 'permissions.view', 'PATCH': 'permissions.edit_permission', 'DELETE': 'permissions.edit_permission'}),
        ('permissions/permissions/',               {'GET': 'permissions.view', 'POST': 'permissions.edit_permission'}),
        ('permissions/endpoints/{id}/',            {'GET': 'permissions.view', 'PATCH': 'permissions.edit_endpoint'}),
        ('permissions/endpoints/',                 'permissions.view'),
    ]
    for prefix, rule in ORDER:
        if p == prefix or p.startswith(prefix):
            if isinstance(rule, str):
                return rule
            return rule.get(method.upper())
    return 'dashboard.view'


def _sync_endpoints_from_urls(Endpoint):
    """URL routing'dan Endpoint jadvaliga hamma /api/ marshrutlarini yozadi (idempotent)."""
    from django.urls import get_resolver, URLPattern, URLResolver

    def _walk(patterns, prefix=''):
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                yield from _walk(pattern.url_patterns, prefix + str(pattern.pattern))
            elif isinstance(pattern, URLPattern):
                route = prefix + str(pattern.pattern)
                route = re.sub(r'<(?:int:|str:|uuid:|slug:|path:)?[a-zA-Z_][a-zA-Z0-9_]*>', '{id}', route)
                route = '/' + route.lstrip('/')
                if not route.endswith('/') and '.' not in route.split('/')[-1]:
                    route += '/'
                yield route, pattern.callback

    HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    try:
        resolver = get_resolver()
    except Exception:
        # URL'lar hali yuklanmagan (masalan, test kontekstida) — o'tkazib yuboramiz.
        return

    for path, callback in _walk(resolver.url_patterns):
        if not path.startswith('/api/'):
            continue
        view_class = getattr(callback, 'view_class', None)
        methods = HTTP_METHODS
        if view_class:
            methods = [m.upper() for m in view_class.http_method_names if m.upper() in HTTP_METHODS]
        for method in methods:
            Endpoint.objects.get_or_create(
                path=path,
                method=method,
                defaults={
                    'name': f'{method} {path}',
                    'access_type': 'authenticated',
                    'is_active': True,
                },
            )


def seed_defaults(apps, schema_editor):
    Permission = apps.get_model('permissions', 'Permission')
    Role = apps.get_model('permissions', 'Role')
    Endpoint = apps.get_model('permissions', 'Endpoint')
    User = apps.get_model('users', 'User')

    # 1) Permissionlar
    perm_by_code: dict = {}
    for codename, name, description, _parent in PERMISSIONS:
        obj, _ = Permission.objects.get_or_create(
            codename=codename,
            defaults={'name': name, 'description': description},
        )
        perm_by_code[codename] = obj
    for codename, _n, _d, parent_code in PERMISSIONS:
        if not parent_code:
            continue
        parent = perm_by_code.get(parent_code)
        child = perm_by_code[codename]
        if parent and child.parent_id != parent.id:
            child.parent = parent
            child.save(update_fields=['parent'])

    # 2) Rollar — yangi rollarga to'liq permission bog'lash, mavjudi bo'sh bo'lsa ham to'ldirish
    role_by_name: dict = {}
    for name, description, codenames in ROLES:
        role, was_created = Role.objects.get_or_create(
            name=name,
            defaults={'description': description, 'is_active': True},
        )
        role_by_name[name] = role

        target = list(perm_by_code.values()) if codenames is None \
            else [perm_by_code[c] for c in codenames if c in perm_by_code]

        # Faqat yangi yaratilgan yoki bo'sh rollarni to'ldiramiz —
        # admin qo'lda tuzgan rollarga tegmaymiz
        if was_created or role.permissions.count() == 0:
            role.permissions.set(target)

    # 3) Endpointlarni URL routing'dan sinxronlash
    _sync_endpoints_from_urls(Endpoint)

    # 4) Admin endpointlarini permission-gated qilish (faqat authenticated bo'lganlar)
    for ep in Endpoint.objects.filter(path__startswith='/api/v1/admin/', access_type='authenticated'):
        codename = _endpoint_permission_for(ep.path, ep.method)
        if not codename:
            continue
        perm = perm_by_code.get(codename)
        if not perm:
            continue
        ep.access_type = 'permission'
        ep.permission = perm
        ep.save(update_fields=['access_type', 'permission'])

    # 5) Mavjud adminlarni rolga biriktirish — faqat rolsizlariga
    super_admin_role = role_by_name.get('Super Admin')
    admin_role = role_by_name.get('Admin')

    for user in User.objects.filter(is_superuser=True):
        if not user.roles.exists() and super_admin_role:
            user.roles.add(super_admin_role)

    for user in User.objects.filter(is_staff=True, is_superuser=False):
        if not user.roles.exists() and admin_role:
            user.roles.add(admin_role)


def reverse_noop(apps, schema_editor):
    """
    Migrationni ortga qaytarish default ma'lumotlarni o'chirmaydi —
    admin qo'lda o'chirsin, aks holda ishlab turgan sozlamalar yo'qoladi.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_defaults, reverse_noop),
    ]
