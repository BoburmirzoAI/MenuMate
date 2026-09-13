from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('users/', include('apps.users.urls.v1', namespace='users')),
    path('devices/', include('apps.devices.urls.v1', namespace='devices')),
    path('referrals/', include('apps.referrals.urls.v1', namespace='referrals')),
    path('family/', include('apps.family.urls.v1', namespace='family')),
    path('recipes/', include('apps.recipes.urls.v1', namespace='recipes')),
    path('menu/', include('apps.menu.urls.v1', namespace='menu')),
    path('products/', include('apps.products.urls.v1', namespace='products')),
    path('weather/', include('apps.weather.urls.v1', namespace='weather')),
    path('notifications/', include('apps.notifications.urls.v1', namespace='notifications')),
]
