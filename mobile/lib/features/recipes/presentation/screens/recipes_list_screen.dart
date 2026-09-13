import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/food_image.dart';
import '../../../../core/widgets/section_card.dart';
import '../../../../core/widgets/state_views.dart';
import '../../data/recipes_repository.dart';
import '../../domain/recipe.dart';

/// Retseptlar ro'yxati — kategoriya filter + search.
class RecipesListScreen extends ConsumerStatefulWidget {
  const RecipesListScreen({super.key});

  @override
  ConsumerState<RecipesListScreen> createState() => _RecipesListScreenState();
}

class _RecipesListScreenState extends ConsumerState<RecipesListScreen> {
  final _searchCtrl = TextEditingController();

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final filters = ref.watch(recipeFiltersProvider);
    final recipesAsync = ref.watch(recipesListProvider);

    return Scaffold(
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Padding(
              padding: const EdgeInsets.fromLTRB(
                AppSpacing.xxl, AppSpacing.lg, AppSpacing.xxl, AppSpacing.md,
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const DisplayTitle('Retseptlar', size: 30),
                  const SizedBox(height: 4),
                  Text(
                    recipesAsync.when(
                      data: (r) => "${r.totalItems} ta ovqat",
                      loading: () => "Yuklanmoqda...",
                      error: (_, _) => "Xato",
                    ),
                    style: TextStyle(color: AppColors.textMedium, fontSize: 14),
                  ),
                ],
              ),
            ),

            // Search
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
              child: TextField(
                controller: _searchCtrl,
                onSubmitted: (v) {
                  ref.read(recipeFiltersProvider.notifier)
                      .update(filters.copyWith(search: v));
                },
                decoration: InputDecoration(
                  hintText: 'Retsept qidirish...',
                  prefixIcon: const Icon(Icons.search, size: 22),
                  suffixIcon: _searchCtrl.text.isNotEmpty
                      ? IconButton(
                          icon: const Icon(Icons.clear, size: 20),
                          onPressed: () {
                            _searchCtrl.clear();
                            ref.read(recipeFiltersProvider.notifier)
                                .update(filters.copyWith(search: ''));
                          },
                        )
                      : null,
                ),
              ),
            ),

            // Category chips
            const SizedBox(height: AppSpacing.md),
            SizedBox(
              height: 40,
              child: ListView(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
                children: [
                  _CategoryChip(
                    label: 'Barchasi',
                    emoji: '🍽️',
                    selected: filters.category == null,
                    onTap: () {
                      ref.read(recipeFiltersProvider.notifier)
                          .update(filters.copyWith(clearCategory: true));
                    },
                  ),
                  const SizedBox(width: 8),
                  for (final entry in RecipeCategoryInfo.map.entries) ...[
                    _CategoryChip(
                      label: entry.value.$2,
                      emoji: entry.value.$1,
                      selected: filters.category == entry.key,
                      onTap: () {
                        ref.read(recipeFiltersProvider.notifier)
                            .update(filters.copyWith(category: entry.key));
                      },
                    ),
                    const SizedBox(width: 8),
                  ],
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.md),
            // List
            Expanded(
              child: recipesAsync.when(
                loading: () => const LoadingView(),
                error: (err, _) => ErrorRetryView(
                  message: err is ApiException ? err.message : '$err',
                  onRetry: () => ref.invalidate(recipesListProvider),
                ),
                data: (result) {
                  if (result.results.isEmpty) return const _EmptyView();
                  return RefreshIndicator(
                    onRefresh: () async => ref.invalidate(recipesListProvider),
                    child: ListView.separated(
                      padding: const EdgeInsets.all(AppSpacing.xxl),
                      itemCount: result.results.length,
                      separatorBuilder: (_, _) => const SizedBox(height: AppSpacing.md),
                      itemBuilder: (context, i) => _RecipeCard(recipe: result.results[i]),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _CategoryChip extends StatelessWidget {
  const _CategoryChip({
    required this.label,
    required this.emoji,
    required this.selected,
    required this.onTap,
  });
  final String label;
  final String emoji;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: selected ? AppColors.terracotta : AppColors.creamCard,
          borderRadius: BorderRadius.circular(AppRadius.pill),
        ),
        child: Row(
          children: [
            Text(emoji, style: const TextStyle(fontSize: 16)),
            const SizedBox(width: 6),
            Text(
              label,
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: selected ? Colors.white : AppColors.textDark,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _RecipeCard extends StatelessWidget {
  const _RecipeCard({required this.recipe});
  final Recipe recipe;

  @override
  Widget build(BuildContext context) {
    return SectionCard(
      color: Colors.white,
      padding: const EdgeInsets.all(AppSpacing.lg),
      onTap: () => context.push('/recipes/${recipe.id}'),
      child: Row(
        children: [
          FoodImage(
            imageUrl: recipe.imageUrl,
            emoji: RecipeCategoryInfo.emoji(recipe.category),
            size: 64,
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  recipe.name,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                    color: AppColors.textDark,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 4),
                Text(
                  RecipeCategoryInfo.label(recipe.category),
                  style: const TextStyle(
                    fontSize: 12,
                    color: AppColors.textLight,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 6),
                Row(
                  children: [
                    _InfoDot(icon: Icons.local_fire_department, text: '${recipe.caloriesPerServing} kcal'),
                    const SizedBox(width: 10),
                    _InfoDot(icon: Icons.schedule, text: '${recipe.prepTimeMinutes} daq'),
                    if (recipe.allergenTags.isNotEmpty) ...[
                      const SizedBox(width: 10),
                      Icon(Icons.warning_amber_rounded, size: 12, color: AppColors.warning),
                      const SizedBox(width: 2),
                      Text(
                        '${recipe.allergenTags.length}',
                        style: const TextStyle(fontSize: 11, color: AppColors.warning, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ],
                ),
              ],
            ),
          ),
          const Icon(Icons.arrow_forward_ios, size: 14, color: AppColors.textLight),
        ],
      ),
    );
  }
}

class _InfoDot extends StatelessWidget {
  const _InfoDot({required this.icon, required this.text});
  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 12, color: AppColors.textLight),
        const SizedBox(width: 3),
        Text(
          text,
          style: const TextStyle(fontSize: 11, color: AppColors.textLight, fontWeight: FontWeight.w500),
        ),
      ],
    );
  }
}

class _EmptyView extends ConsumerWidget {
  const _EmptyView();
  @override
  Widget build(BuildContext context, WidgetRef ref) => EmptyView(
        emoji: '🔍',
        title: ref.tr('recipes_empty_title'),
        subtitle: ref.tr('recipes_empty_body'),
      );
}
