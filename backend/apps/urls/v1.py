from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    # ═══ Foydalanuvchi API'lari ═══
    path('users/', include('apps.users.urls.v1', namespace='users')),
    path('devices/', include('apps.devices.urls.v1', namespace='devices')),
    path('referrals/', include('apps.referrals.urls.v1', namespace='referrals')),
    path('family/', include('apps.family.urls.v1', namespace='family')),
    path('recipes/', include('apps.recipes.urls.v1', namespace='recipes')),
    path('menu/', include('apps.menu.urls.v1', namespace='menu')),
    path('products/', include('apps.products.urls.v1', namespace='products')),
    path('weather/', include('apps.weather.urls.v1', namespace='weather')),
    path('notifications/', include('apps.notifications.urls.v1', namespace='notifications')),

    # ═══ Admin API'lari (React admin paneli uchun) ═══
    path('admin/', include('apps.shared.urls.admin', namespace='admin-shared')),
    path('admin/users/', include('apps.users.urls.admin', namespace='admin-users')),
    path('admin/families/', include('apps.family.urls.admin', namespace='admin-families')),
    path('admin/recipes/', include('apps.recipes.urls.admin', namespace='admin-recipes')),
    path('admin/menus/', include('apps.menu.urls.admin', namespace='admin-menus')),
    path('admin/shopping/', include('apps.products.urls.admin', namespace='admin-shopping')),
    path('admin/notifications/', include('apps.notifications.urls.admin', namespace='admin-notifications')),
    path('admin/devices/', include('apps.devices.urls.admin', namespace='admin-devices')),
    path('admin/weather/', include('apps.weather.urls.admin', namespace='admin-weather')),
    path('admin/permissions/', include('apps.permissions.urls.admin', namespace='admin-permissions')),
]
