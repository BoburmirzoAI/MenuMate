import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/api/simple_repositories.dart' show shoppingListProvider;
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/food_image.dart';
import '../../../../core/widgets/section_card.dart';
import '../../data/menu_repository.dart';
import '../../domain/menu.dart';

/// Kun detali — foydalanuvchi har mahal (nonushta/tushlik/kechki) uchun
/// bo'limlar (asosiy/salat/ichimlik va h.k.) bo'yicha retsept tanlaydi.
class DayDetailScreen extends ConsumerWidget {
  const DayDetailScreen({super.key, required this.menuId, required this.dayId});

  final int menuId;
  final int dayId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final menuAsync = ref.watch(currentMenuProvider);

    return Scaffold(
      appBar: AppBar(title: Text(ref.tr('day_detail_title'))),
      body: menuAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, _) => Center(
          child: Text(err is ApiException ? err.message : ref.tr('error')),
        ),
        data: (menu) {
          if (menu == null) return Center(child: Text(ref.tr('menu_empty_title')));
          final day = menu.days.where((d) => d.id == dayId).firstOrNull;
          if (day == null) return Center(child: Text(ref.tr('day_not_found')));

          return SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.xxl),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _DateHeader(day: day),
                const SizedBox(height: AppSpacing.xxl),
                for (final meal in day.meals) ...[
                  _MealSection(meal: meal),
                  const SizedBox(height: AppSpacing.xl),
                ],
                const SizedBox(height: AppSpacing.huge),
              ],
            ),
          );
        },
      ),
    );
  }
}

// ============================================================================
// Sana header
// ============================================================================

class _DateHeader extends StatelessWidget {
  const _DateHeader({required this.day});
  final MenuDay day;

  @override
  Widget build(BuildContext context) {
    final dayLabel = DateFormat('EEEE', 'uz').format(day.date);
    final subtitle = DateFormat('d MMMM yyyy', 'uz').format(day.date);

    return SectionCard(
      color: day.isHoliday ? AppColors.creamAccent : AppColors.creamCard,
      padding: const EdgeInsets.all(AppSpacing.xl),
      child: Row(
        children: [
          Container(
            width: 64, height: 64,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(AppRadius.lg),
            ),
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  DateFormat('dd').format(day.date),
                  style: const TextStyle(
                    fontSize: 22, fontWeight: FontWeight.w700,
                    color: AppColors.textDark,
                  ),
                ),
                Text(
                  DateFormat('MMM', 'uz').format(day.date),
                  style: const TextStyle(fontSize: 10, color: AppColors.textLight),
                ),
              ],
            ),
          ),
          const SizedBox(width: AppSpacing.lg),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                DisplayTitle(dayLabel, size: 20),
                const SizedBox(height: 2),
                Text(subtitle, style: TextStyle(color: AppColors.textMedium, fontSize: 13)),
                if (day.isHoliday) ...[
                  const SizedBox(height: 6),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                    decoration: BoxDecoration(
                      color: AppColors.saffron,
                      borderRadius: BorderRadius.circular(AppRadius.pill),
                    ),
                    child: Text(
                      '🎉 ${day.holidayName}',
                      style: const TextStyle(
                        fontSize: 11, fontWeight: FontWeight.w700, color: Colors.white,
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ============================================================================
// Meal section (Nonushta / Tushlik / Kechki)
// ============================================================================

/// Slot kategoriyasi meta.
class _SlotSpec {
  const _SlotSpec(this.category, this.label, this.emoji);
  final String category;
  final String label;
  final String emoji;
}

// Slot label — translation kalitiga bog'lanadi (ref.tr).
// _SlotSpec.label endi kalit deb qaraladi (masalan 'meal_slot_main').
const _slotsForMeal = <String, List<_SlotSpec>>{
  'BREAKFAST': [
    _SlotSpec('MAIN', 'meal_slot_main', '🍳'),
    _SlotSpec('DRINK', 'meal_slot_drink', '🥤'),
    _SlotSpec('BREAD', 'meal_slot_bread', '🥖'),
    _SlotSpec('DESSERT', 'meal_slot_dessert', '🍰'),
  ],
  'LUNCH': [
    _SlotSpec('MAIN', 'meal_slot_main', '🍲'),
    _SlotSpec('SOUP', 'meal_slot_soup', '🥣'),
    _SlotSpec('SALAD', 'meal_slot_salad', '🥗'),
    _SlotSpec('DRINK', 'meal_slot_drink', '🥤'),
    _SlotSpec('BREAD', 'meal_slot_bread', '🥖'),
    _SlotSpec('DESSERT', 'meal_slot_dessert', '🍰'),
  ],
  'DINNER': [
    _SlotSpec('MAIN', 'meal_slot_main', '🍽️'),
    _SlotSpec('SOUP', 'meal_slot_soup', '🥣'),
    _SlotSpec('SALAD', 'meal_slot_salad', '🥗'),
    _SlotSpec('DRINK', 'meal_slot_drink', '🥤'),
    _SlotSpec('BREAD', 'meal_slot_bread', '🥖'),
    _SlotSpec('DESSERT', 'meal_slot_dessert', '🍰'),
  ],
};

const _mealTypeLabelKey = {
  'BREAKFAST': 'meal_breakfast',
  'LUNCH': 'meal_lunch',
  'DINNER': 'meal_dinner',
};
const _mealTypeEmoji = {
  'BREAKFAST': '☕',
  'LUNCH': '🍲',
  'DINNER': '🍽️',
};

class _MealSection extends ConsumerWidget {
  const _MealSection({required this.meal});
  final MenuMeal meal;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final slots = _slotsForMeal[meal.mealType] ?? const <_SlotSpec>[];
    return SectionCard(
      color: Colors.white,
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(
                _mealTypeEmoji[meal.mealType] ?? '🍴',
                style: const TextStyle(fontSize: 22),
              ),
              const SizedBox(width: 8),
              Text(
                ref.tr(_mealTypeLabelKey[meal.mealType] ?? 'meal'),
                style: const TextStyle(
                  fontSize: 16, fontWeight: FontWeight.w700, color: AppColors.textDark,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          for (int i = 0; i < slots.length; i++) ...[
            _SlotRow(
              meal: meal,
              spec: slots[i],
              existing: meal.itemFor(slots[i].category),
            ),
            if (i != slots.length - 1) const Divider(height: 1),
          ],
        ],
      ),
    );
  }
}

class _SlotRow extends ConsumerWidget {
  const _SlotRow({required this.meal, required this.spec, required this.existing});

  final MenuMeal meal;
  final _SlotSpec spec;
  final MenuMealItem? existing;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isFilled = existing != null;
    return InkWell(
      onTap: () => _openPicker(context, ref),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 10),
        child: Row(
          children: [
            FoodImage(
              imageUrl: existing?.recipe.imageUrl ?? '',
              emoji: spec.emoji,
              size: 42,
              radius: AppRadius.sm,
              background: AppColors.creamCard,
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    ref.tr(spec.label),
                    style: TextStyle(
                      fontSize: 11, fontWeight: FontWeight.w700,
                      color: AppColors.textLight, letterSpacing: 0.6,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    existing?.recipe.name ?? ref.tr('slot_add_pick'),
                    style: TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w600,
                      color: isFilled ? AppColors.textDark : AppColors.terracotta,
                      fontStyle: isFilled ? FontStyle.normal : FontStyle.normal,
                    ),
                  ),
                ],
              ),
            ),
            if (isFilled)
              IconButton(
                icon: const Icon(Icons.close, size: 18, color: AppColors.textLight),
                onPressed: () => _remove(context, ref),
                tooltip: 'Olib tashlash',
              )
            else
              const Icon(Icons.add_circle_outline, color: AppColors.terracotta),
          ],
        ),
      ),
    );
  }

  Future<void> _openPicker(BuildContext context, WidgetRef ref) async {
    final picked = await showModalBottomSheet<RecipeShort>(
      context: context,
      isScrollControlled: true,
      backgroundColor: AppColors.creamBg,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(AppRadius.xxl)),
      ),
      builder: (_) => _RecipePickerSheet(
        mealId: meal.id,
        category: spec.category,
        title: ref.tr(spec.label),
      ),
    );
    if (picked == null || !context.mounted) return;

    try {
      await ref.read(menuRepositoryProvider).addItem(
            mealId: meal.id,
            category: spec.category,
            recipeId: picked.id,
          );
      ref.invalidate(currentMenuProvider);
      ref.invalidate(shoppingListProvider);
    } on ApiException catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
    }
  }

  Future<void> _remove(BuildContext context, WidgetRef ref) async {
    final item = existing;
    if (item == null) return;
    try {
      await ref.read(menuRepositoryProvider).removeItem(
            mealId: meal.id, itemId: item.id,
          );
      ref.invalidate(currentMenuProvider);
      ref.invalidate(shoppingListProvider);
    } on ApiException catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
    }
  }
}

// ============================================================================
// Recipe picker bottom sheet
// ============================================================================

class _RecipePickerSheet extends ConsumerWidget {
  const _RecipePickerSheet({
    required this.mealId,
    required this.category,
    required this.title,
  });

  final int mealId;
  final String category;
  final String title;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final recsAsync = ref.watch(_recommendationsProvider((mealId, category)));

    return DraggableScrollableSheet(
      expand: false,
      initialChildSize: 0.7,
      minChildSize: 0.4,
      maxChildSize: 0.9,
      builder: (_, controller) => Column(
        children: [
          // Grabber
          Container(
            margin: const EdgeInsets.only(top: 8, bottom: 4),
            width: 40, height: 4,
            decoration: BoxDecoration(
              color: AppColors.textLight.withValues(alpha: 0.3),
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(
              AppSpacing.xxl, AppSpacing.md, AppSpacing.xxl, AppSpacing.sm,
            ),
            child: Row(
              children: [
                Expanded(child: DisplayTitle('$title · ${ref.tr('picker_title_suffix')}', size: 22)),
                Text(
                  ref.tr('picker_recommended'),
                  style: TextStyle(
                    fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textMedium,
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: recsAsync.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, _) => Center(
                child: Text(err is ApiException ? err.message : ref.tr('error')),
              ),
              data: (recipes) {
                if (recipes.isEmpty) {
                  return Center(
                    child: Padding(
                      padding: const EdgeInsets.all(AppSpacing.xxl),
                      child: Text(
                        ref.tr('picker_empty'),
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: AppColors.textMedium),
                      ),
                    ),
                  );
                }
                return ListView.separated(
                  controller: controller,
                  padding: const EdgeInsets.all(AppSpacing.xxl),
                  itemCount: recipes.length,
                  separatorBuilder: (_, _) => const SizedBox(height: AppSpacing.md),
                  itemBuilder: (context, i) => _RecipeChoice(
                    recipe: recipes[i],
                    onPick: () => Navigator.of(context).pop(recipes[i]),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _RecipeChoice extends StatelessWidget {
  const _RecipeChoice({required this.recipe, required this.onPick});
  final RecipeShort recipe;
  final VoidCallback onPick;

  @override
  Widget build(BuildContext context) {
    return SectionCard(
      color: Colors.white,
      padding: const EdgeInsets.all(AppSpacing.lg),
      onTap: onPick,
      child: Row(
        children: [
          FoodImage(
            imageUrl: recipe.imageUrl,
            emoji: _categoryEmoji(recipe.category),
            size: 52,
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  recipe.name,
                  style: const TextStyle(
                    fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.textDark,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 4),
                Row(
                  children: [
                    _dot(Icons.local_fire_department, '${recipe.caloriesPerServing} kcal'),
                    const SizedBox(width: 10),
                    _dot(Icons.schedule, '${recipe.prepTimeMinutes} daq'),
                  ],
                ),
              ],
            ),
          ),
          const Icon(Icons.check_circle_outline, color: AppColors.terracotta),
        ],
      ),
    );
  }

  Widget _dot(IconData icon, String label) => Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 12, color: AppColors.textLight),
          const SizedBox(width: 3),
          Text(label, style: const TextStyle(fontSize: 11, color: AppColors.textLight)),
        ],
      );

  String _categoryEmoji(String category) {
    switch (category) {
      case 'BREAKFAST': return '☕';
      case 'LUNCH': return '🍲';
      case 'DINNER': return '🍽️';
      case 'SALAD': return '🥗';
      case 'SOUP': return '🥣';
      case 'DRINK': return '🥤';
      case 'DESSERT': return '🍰';
      case 'BREAD': return '🥖';
      case 'SNACK': return '🍿';
      default: return '🍴';
    }
  }
}

// ============================================================================
// Recommendations provider
// ============================================================================

final _recommendationsProvider = FutureProvider.autoDispose
    .family<List<RecipeShort>, (int, String)>((ref, key) async {
  final (mealId, category) = key;
  return ref.watch(menuRepositoryProvider).getRecommendations(
        mealId: mealId, category: category,
      );
});
