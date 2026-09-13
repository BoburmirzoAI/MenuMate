from django.contrib import admin

from apps.menu.models.menu import Menu, MenuDay, MenuMeal, MenuMealItem


class MenuMealItemInline(admin.TabularInline):
    model = MenuMealItem
    extra = 0
    autocomplete_fields = ('recipe',)


class MenuMealInline(admin.TabularInline):
    model = MenuMeal
    extra = 0
    show_change_link = True
    fields = ('meal_type',)


class MenuDayInline(admin.TabularInline):
    model = MenuDay
    extra = 0
    show_change_link = True
    fields = ('date', 'is_holiday', 'holiday_name')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'family', 'start_date', 'end_date', 'duration', 'status', 'created_at')
    list_filter = ('duration', 'status')
    search_fields = ('family__family_name', 'family__user__email')
    list_select_related = ('family',)
    inlines = [MenuDayInline]


@admin.register(MenuDay)
class MenuDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu', 'date', 'is_holiday', 'holiday_name')
    list_filter = ('is_holiday',)
    list_select_related = ('menu',)
    inlines = [MenuMealInline]


@admin.register(MenuMeal)
class MenuMealAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', 'meal_type')
    list_filter = ('meal_type',)
    list_select_related = ('day',)
    inlines = [MenuMealItemInline]


@admin.register(MenuMealItem)
class MenuMealItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'meal', 'category', 'recipe')
    list_filter = ('category',)
    list_select_related = ('meal', 'recipe')
