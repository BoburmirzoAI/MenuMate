from django.urls import path

from apps.products.views.products import ShoppingItemToggleAPIView

app_name = 'products'

urlpatterns = [
    # /shopping-items/<id>/  — bitta item toggle (is_purchased)
    path('shopping-items/<int:item_id>/',
         ShoppingItemToggleAPIView.as_view(), name='item-toggle'),
]
