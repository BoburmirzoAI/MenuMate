"""
python manage.py seed_permissions

Default permissionlar, rollarni yaratadi va `/api/v1/admin/*` endpointlarini
tegishli permission'ga bog'laydi. Idempotent — mavjud yozuvlarni buzmaydi.

Ishlatilishi:
    python manage.py sync_endpoints
    python manage.py seed_permissions

Rollar:
    - Super Admin — hamma permissionlar
    - Admin       — kontent va foydalanuvchi boshqaruvi (RBAC'dan tashqari)
    - Moderator   — retseptlar, ingredientlar, bayramlar, xabarlar
    - User        — admin panelga kirmaydi
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.permissions.models.permissions import Endpoint, Permission, Role


PERMISSIONS: list[tuple[str, str, str, str | None]] = [
    ('dashboard.view',              'Dashboard ko\'rish',           'Admin panel bosh sahifasini ko\'rish', None),

    ('users.manage',                'Foydalanuvchilarni boshqarish', 'Foydalanuvchilar ustidan to\'liq nazorat', None),
    ('users.view',                  'Foydalanuvchilarni ko\'rish',   'Foydalanuvchilar ro\'yxati va profilini ko\'rish', 'users.manage'),
    ('users.create',                'Foydalanuvchi yaratish',        'Yangi foydalanuvchi qo\'shish',                    'users.manage'),
    ('users.edit',                  'Foydalanuvchi tahrirlash',      'Profil, rol va parolni yangilash',                 'users.manage'),
    ('users.delete',                'Foydalanuvchi o\'chirish',      'Foydalanuvchini soft-delete qilish',               'users.manage'),

    ('families.manage',             'Oilalarni boshqarish',          'Oila profillari va a\'zolar',                      None),
    ('families.view',               'Oilalarni ko\'rish',            'Oila ro\'yxati va tafsilotlarini ko\'rish',        'families.manage'),
    ('families.edit',               'Oila tahrirlash',               'Oila nomi, shahar va a\'zolarni o\'zgartirish',    'families.manage'),
    ('families.delete',             'Oila o\'chirish',               'Oilani va a\'zolarini o\'chirish',                 'families.manage'),

    ('recipes.manage',              'Retseptlarni boshqarish',       'Retseptlar ustidan to\'liq nazorat',               None),
    ('recipes.view',                'Retseptlarni ko\'rish',         'Retseptlar ro\'yxatini ko\'rish',                  'recipes.manage'),
    ('recipes.create',              'Retsept yaratish',              'Yangi retsept qo\'shish',                          'recipes.manage'),
    ('recipes.edit',                'Retsept tahrirlash',            'Retseptni yangilash',                              'recipes.manage'),
    ('recipes.delete',              'Retsept o\'chirish',            'Retseptni o\'chirish',                             'recipes.manage'),

    ('ingredients.manage',          'Ingredientlarni boshqarish',    'Ingredient katalogi ustidan nazorat',              None),
    ('ingredients.view',            'Ingredientlarni ko\'rish',      'Ingredient ro\'yxatini ko\'rish',                  'ingredients.manage'),
    ('ingredients.create',          'Ingredient yaratish',           'Yangi ingredient qo\'shish',                       'ingredients.manage'),
    ('ingredients.edit',            'Ingredient tahrirlash',         'Ingredientni yangilash',                           'ingredients.manage'),
    ('ingredients.delete',          'Ingredient o\'chirish',         'Ingredientni o\'chirish',                          'ingredients.manage'),

    ('menus.manage',                'Menyularni boshqarish',         'Foydalanuvchi menyularini kuzatish/o\'chirish',    None),
    ('menus.view',                  'Menyularni ko\'rish',           'Barcha menyular ro\'yxatini ko\'rish',             'menus.manage'),
    ('menus.delete',                'Menyu o\'chirish',              'Menyuni o\'chirish',                               'menus.manage'),

    ('notifications.manage',        'Bildirishnomalarni boshqarish', 'Push va broadcast xabarlar',                       None),
    ('notifications.view',          'Bildirishnomalarni ko\'rish',   'Push tarixini ko\'rish',                           'notifications.manage'),
    ('notifications.broadcast',     'Bildirishnoma yuborish',        'Ommaviy push xabar',                               'notifications.manage'),

    ('holidays.manage',             'Bayramlarni boshqarish',        'Milliy va oilaviy bayramlar',                      None),
    ('holidays.view',               'Bayramlarni ko\'rish',          'Bayramlar ro\'yxati',                              'holidays.manage'),
    ('holidays.create',             'Bayram yaratish',               'Yangi bayram qo\'shish',                           'holidays.manage'),
    ('holidays.edit',               'Bayram tahrirlash',             'Bayramni yangilash',                               'holidays.manage'),
    ('holidays.delete',             'Bayram o\'chirish',             'Bayramni o\'chirish',                              'holidays.manage'),

    ('devices.view',                'Qurilmalarni ko\'rish',         'Ro\'yxatga olingan qurilmalar va FCM tokenlar',    None),

    ('weather.manage',              'Ob-havoni boshqarish',          'Ob-havo cache holati',                             None),
    ('weather.view',                'Ob-havo cache ko\'rish',        'Snapshot yozuvlari',                               'weather.manage'),
    ('weather.clear',               'Ob-havo cache tozalash',        'Cache\'ni bo\'shatish',                            'weather.manage'),

    ('permissions.manage',          'Ruxsat tizimini boshqarish',    'Rollar, permissionlar, endpoint sozlamalari',      None),
    ('permissions.view',            'Ruxsatlarni ko\'rish',          'Rollar/permissionlar/endpointlarni ko\'rish',      'permissions.manage'),
    ('permissions.edit_role',       'Rolni tahrirlash',              'Rol yaratish/o\'chirish/o\'zgartirish',            'permissions.manage'),
    ('permissions.edit_permission', 'Permissionni tahrirlash',       'Permission yaratish/o\'zgartirish',                'permissions.manage'),
    ('permissions.edit_endpoint',   'Endpointni sozlash',            'Endpoint access_type\'ni o\'zgartirish',           'permissions.manage'),

    ('stats.view',                  'Statistika ko\'rish',           'KPI va tizim ko\'rsatkichlari',                    None),
]


ROLES: list[tuple[str, str, list[str] | None]] = [
    (
        'Super Admin',
        'Barcha huquqlarga ega. RBAC boshqaruvi bilan ishlaydi.',
        None,
    ),
    (
        'Admin',
        'Kontent va foydalanuvchi boshqaruvi. Ruxsat tizimiga tegmaydi.',
        [
            'dashboard.view', 'stats.view',
            'users.manage', 'families.manage',
            'recipes.manage', 'ingredients.manage',
            'menus.manage', 'notifications.manage',
            'holidays.manage', 'devices.view', 'weather.manage',
            'permissions.view',
        ],
    ),
    (
        'Moderator',
        'Kontent tayyorlaydi — retseptlar, ingredientlar, bayramlar, xabarlar.',
        [
            'dashboard.view', 'stats.view',
            'recipes.manage', 'ingredients.manage',
            'holidays.manage', 'notifications.broadcast',
        ],
    ),
    (
        'User',
        'Oddiy foydalanuvchi — admin panelga kirmaydi.',
        [],
    ),
]


def endpoint_permission_for(path: str, method: str) -> str | None:
    """/api/v1/admin/* uchun tegishli permission codename qaytaradi.

    Path prefix va HTTP metod bo'yicha aniqlaydi. Uzunroq prefixlar avval
    tekshiriladi (aniqroq moslik). Boshqa admin endpointlari uchun default
    sifatida `dashboard.view` qaytadi.
    """
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


class Command(BaseCommand):
    help = 'Default permissionlar, rollar va admin endpoint sozlamalarini yaratadi (idempotent).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reassign-endpoints',
            action='store_true',
            help="Admin endpointlarining access_type va permission'ini qayta hisoblab yozadi.",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        self.stdout.write(self.style.MIGRATE_HEADING('1) Permissionlar'))
        perms = self._seed_permissions()

        self.stdout.write(self.style.MIGRATE_HEADING('2) Rollar'))
        self._seed_roles(perms)

        self.stdout.write(self.style.MIGRATE_HEADING('3) Admin endpointlarini sozlash'))
        self._configure_admin_endpoints(perms, reassign=opts['reassign_endpoints'])

        self.stdout.write(self.style.SUCCESS('\n✓ Seed tugadi.'))

    def _seed_permissions(self) -> dict[str, Permission]:
        """PERMISSIONS ro'yxati bo'yicha Permission yozuvlarini yaratadi/yangilaydi.

        Ikki bosqichli: avval parent'siz qatorda hammasi yaratiladi, keyin
        parent link'lar bog'lanadi. Bu tartib parent hali yozilmagan holatda
        child yozilishini oldini oladi. Codename → Permission dict qaytaradi.
        """
        created, updated = 0, 0
        parents: dict[str, str | None] = {}
        objs: dict[str, Permission] = {}

        for codename, name, description, parent_code in PERMISSIONS:
            parents[codename] = parent_code
            obj, was_created = Permission.objects.get_or_create(
                codename=codename,
                defaults={'name': name, 'description': description},
            )
            if not was_created:
                changed = False
                if obj.name != name:
                    obj.name = name
                    changed = True
                if obj.description != description:
                    obj.description = description
                    changed = True
                if changed:
                    obj.save(update_fields=['name', 'description'])
                    updated += 1
            else:
                created += 1
            objs[codename] = obj

        for codename, parent_code in parents.items():
            if not parent_code:
                continue
            parent = objs.get(parent_code)
            child = objs[codename]
            if parent and child.parent_id != parent.id:
                child.parent = parent
                child.save(update_fields=['parent'])

        self.stdout.write(f"   yaratildi: {created}, yangilandi: {updated}, jami: {len(objs)}")
        return objs

    def _seed_roles(self, perms: dict[str, Permission]) -> None:
        """ROLES ro'yxati bo'yicha rollarni yaratadi va permissionlarni bog'laydi.

        Default rollarga M2M `set()` qo'llanadi — bu admin qo'lda default rol
        ustida qilgan o'zgarishlarini bekor qiladi. Boshqa (default emas)
        rollarga tegilmaydi.
        """
        for name, description, codenames in ROLES:
            role, was_created = Role.objects.get_or_create(
                name=name,
                defaults={'description': description, 'is_active': True},
            )
            if not was_created and not role.description:
                role.description = description
                role.save(update_fields=['description'])

            if codenames is None:
                target = list(perms.values())
            else:
                target = [perms[c] for c in codenames if c in perms]

            role.permissions.set(target)
            self.stdout.write(
                f"   {'+ yaratildi' if was_created else '~ yangilandi'}: "
                f"{role.name} ({len(target)} permission)"
            )

    def _configure_admin_endpoints(
        self,
        perms: dict[str, Permission],
        *,
        reassign: bool,
    ) -> None:
        """/api/v1/admin/* endpointlarini permission-gated qilib belgilaydi.

        Faqat `access_type='authenticated'` bo'lgan endpointlarga tegadi — admin
        qo'lda `public` yoki boshqa permission qilib qo'yganlari saqlanadi.
        `reassign=True` bilan majburiy qayta yoziladi.
        """
        qs = Endpoint.objects.filter(path__startswith='/api/v1/admin/')
        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.WARNING(
                "   Ogohlantirish: /api/v1/admin/* endpointlari topilmadi. "
                "Avval `python manage.py sync_endpoints` ishlating."
            ))
            return

        touched, skipped = 0, 0
        for ep in qs.select_related('permission'):
            codename = endpoint_permission_for(ep.path, ep.method)
            if not codename:
                skipped += 1
                continue
            perm = perms.get(codename)
            if not perm:
                skipped += 1
                continue

            needs_update = reassign or ep.access_type != 'permission' or ep.permission_id is None
            if not needs_update:
                skipped += 1
                continue

            ep.access_type = 'permission'
            ep.permission = perm
            ep.is_active = True
            ep.save(update_fields=['access_type', 'permission', 'is_active'])
            touched += 1

        self.stdout.write(
            f"   admin endpointlar: jami {total}, sozlandi {touched}, tegilmadi {skipped}"
        )
