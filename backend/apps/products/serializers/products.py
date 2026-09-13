"""Shopping list serializerlari — Karzinka Go real integratsiyasi bilan."""
from decimal import Decimal

from rest_framework import serializers

from apps.products.models.products import ShoppingItem, ShoppingList
from apps.products.utils.karzinka import KarzinkaProduct, match_ingredients
from apps.recipes.models.recipes import Ingredient


class NestedIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id', 'name', 'name_uz', 'name_ru', 'name_en',
            'category', 'image_url',
        ]
        read_only_fields = fields


class ShoppingItemSerializer(serializers.ModelSerializer):
    """Har mahsulot uchun context'dagi Karzinka mos mahsuloti (agar bor bo'lsa)."""

    ingredient = NestedIngredientSerializer(read_only=True)
    kgo_available = serializers.SerializerMethodField()
    kgo_price_per_unit = serializers.SerializerMethodField()
    kgo_unit = serializers.SerializerMethodField()
    price_total = serializers.SerializerMethodField()
    kgo_image_url = serializers.SerializerMethodField()
    kgo_product_url = serializers.SerializerMethodField()
    kgo_title = serializers.SerializerMethodField()
    kgo_weight = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingItem
        fields = [
            'id', 'ingredient', 'total_amount', 'unit', 'is_purchased',
            'kgo_available', 'kgo_price_per_unit', 'kgo_unit', 'price_total',
            'kgo_image_url', 'kgo_product_url', 'kgo_title', 'kgo_weight',
        ]
        read_only_fields = [f for f in fields if f != 'is_purchased']

    # ------------------------------------------------------------------
    # Karzinka mahsulot topilgan bo'lsa uni ishlatamiz
    # ------------------------------------------------------------------

    def _kg_product(self, obj) -> KarzinkaProduct | None:
        matches = (self.context or {}).get('karzinka_matches') or {}
        return matches.get(obj.ingredient_id)

    def get_kgo_available(self, obj) -> bool:
        return self._kg_product(obj) is not None

    def get_kgo_price_per_unit(self, obj) -> str | None:
        p = self._kg_product(obj)
        return str(p.price) if p else None

    def get_kgo_unit(self, obj) -> str:
        p = self._kg_product(obj)
        return p.weight_param if p else ''

    def get_price_total(self, obj) -> str | None:
        # Karzinka'da narx — dona uchun (masalan 1 kg pishloq 65000 so'm).
        # Bizning miqdorimiz (masalan 200g) esa asosiy birlikda.
        # Ideal holda per_gramm konversiya kerak, hozircha faqat narxni beramiz —
        # foydalanuvchi mahsulotni shu narxda savatga qo'shadi.
        p = self._kg_product(obj)
        return str(p.price) if p else None

    def get_kgo_image_url(self, obj) -> str:
        p = self._kg_product(obj)
        return p.image_url if p else ''

    def get_kgo_product_url(self, obj) -> str:
        p = self._kg_product(obj)
        return p.product_url if p else ''

    def get_kgo_title(self, obj) -> str:
        p = self._kg_product(obj)
        return (p.title_uz or p.title_ru or p.title_en) if p else ''

    def get_kgo_weight(self, obj) -> str:
        p = self._kg_product(obj)
        return p.weight_param if p else ''


class ShoppingListSerializer(serializers.ModelSerializer):
    items_by_category = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    available_items = serializers.SerializerMethodField()
    unavailable_items = serializers.SerializerMethodField()
    total_estimated_cost = serializers.SerializerMethodField()
    menu_id = serializers.IntegerField(source='menu.id', read_only=True)

    class Meta:
        model = ShoppingList
        fields = [
            'id', 'menu_id',
            'total_estimated_cost',
            'total_items', 'available_items', 'unavailable_items',
            'items_by_category',
            'created_at', 'updated_at',
        ]
        read_only_fields = fields

    # ------------------------------------------------------------------
    # Barcha itemlar uchun bir marta Karzinka matching — cache
    # ------------------------------------------------------------------

    def _matches(self, obj) -> dict:
        cached = getattr(self, '_matches_cache', None)
        if cached is not None:
            return cached
        ingredients = list({it.ingredient for it in obj.items.select_related('ingredient')})
        matches = match_ingredients(ingredients)
        self._matches_cache = matches
        return matches

    def _item_context(self, obj) -> dict:
        return {**(self.context or {}), 'karzinka_matches': self._matches(obj)}

    def get_total_items(self, obj) -> int:
        return obj.items.count()

    def get_available_items(self, obj) -> int:
        matches = self._matches(obj)
        return sum(1 for it in obj.items.all() if it.ingredient_id in matches)

    def get_unavailable_items(self, obj) -> list:
        matches = self._matches(obj)
        items = [it for it in obj.items.select_related('ingredient')
                 if it.ingredient_id not in matches]
        return ShoppingItemSerializer(
            items, many=True, context=self._item_context(obj),
        ).data

    def get_total_estimated_cost(self, obj) -> str:
        matches = self._matches(obj)
        total = Decimal(0)
        for it in obj.items.all():
            p = matches.get(it.ingredient_id)
            if p is not None:
                total += p.price
        return str(total.quantize(Decimal('1')))

    def get_items_by_category(self, obj) -> dict:
        result: dict = {}
        items = obj.items.select_related('ingredient').order_by(
            'ingredient__category', 'ingredient__name_uz',
        )
        ctx = self._item_context(obj)
        for item in items:
            if not item.ingredient or not item.ingredient.category:
                continue
            result.setdefault(item.ingredient.category, []).append(
                ShoppingItemSerializer(item, context=ctx).data
            )
        return result
