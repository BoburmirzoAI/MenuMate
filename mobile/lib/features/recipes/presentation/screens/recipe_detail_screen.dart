import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/food_image.dart';
import '../../../../core/widgets/section_card.dart';
import '../../data/recipes_repository.dart';
import '../../domain/recipe.dart';

class RecipeDetailScreen extends ConsumerWidget {
  const RecipeDetailScreen({super.key, required this.recipeId});
  final int recipeId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final recipeAsync = ref.watch(recipeDetailProvider(recipeId));

    return Scaffold(
      body: recipeAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, _) => Scaffold(
          appBar: AppBar(),
          body: Center(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.xxl),
              child: Text(err is ApiException ? err.message : 'Xato yuz berdi',
                  textAlign: TextAlign.center),
            ),
          ),
        ),
        data: (recipe) => _RecipeContent(recipe: recipe),
      ),
    );
  }
}

class _RecipeContent extends StatelessWidget {
  const _RecipeContent({required this.recipe});
  final Recipe recipe;

  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      slivers: [
        // App bar — katta rasm hero
        SliverAppBar(
          expandedHeight: 280,
          pinned: true,
          backgroundColor: AppColors.creamCard,
          foregroundColor: AppColors.textDark,
          flexibleSpace: FlexibleSpaceBar(
            background: recipe.hasImage
                ? Stack(fit: StackFit.expand, children: [
                    Image.network(
                      recipe.imageUrl, fit: BoxFit.cover,
                      errorBuilder: (_, _, _) => Container(
                        color: AppColors.creamCard,
                        alignment: Alignment.center,
                        child: Text(
                          RecipeCategoryInfo.emoji(recipe.category),
                          style: const TextStyle(fontSize: 120),
                        ),
                      ),
                    ),
                    Positioned(
                      left: 0, right: 0, bottom: 0, height: 60,
                      child: Container(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            begin: Alignment.topCenter,
                            end: Alignment.bottomCenter,
                            colors: [
                              Colors.transparent,
                              AppColors.creamBg.withValues(alpha: 0.9),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ])
                : Container(
                    color: AppColors.creamCard,
                    alignment: Alignment.center,
                    child: Text(
                      RecipeCategoryInfo.emoji(recipe.category),
                      style: const TextStyle(fontSize: 120),
                    ),
                  ),
          ),
        ),

        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.xxl),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Category chip
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.terracotta.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(AppRadius.sm),
                  ),
                  child: Text(
                    RecipeCategoryInfo.label(recipe.category),
                    style: const TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w700,
                      color: AppColors.terracotta,
                      letterSpacing: 0.5,
                    ),
                  ),
                ),
                const SizedBox(height: AppSpacing.md),

                DisplayTitle(recipe.name, size: 30),

                if (recipe.description.isNotEmpty) ...[
                  const SizedBox(height: AppSpacing.md),
                  Text(
                    recipe.description,
                    style: TextStyle(color: AppColors.textMedium, fontSize: 14, height: 1.5),
                  ),
                ],

                const SizedBox(height: AppSpacing.xl),

                // Info badges (kcal, time, servings, hot/cold)
                Wrap(
                  spacing: 12,
                  runSpacing: 12,
                  children: [
                    _BigBadge(
                      icon: Icons.local_fire_department,
                      value: '${recipe.caloriesPerServing}',
                      label: 'kcal',
                      color: AppColors.terracotta,
                    ),
                    _BigBadge(
                      icon: Icons.schedule,
                      value: '${recipe.prepTimeMinutes}',
                      label: 'daqiqa',
                      color: AppColors.saffron,
                    ),
                    _BigBadge(
                      icon: Icons.person_outline,
                      value: '${recipe.servings}',
                      label: 'kishi',
                      color: AppColors.success,
                    ),
                    _BigBadge(
                      icon: recipe.isHot ? Icons.whatshot : Icons.ac_unit,
                      value: recipe.isHot ? 'Issiq' : 'Salqin',
                      label: 'ovqat',
                      color: recipe.isHot ? AppColors.terracottaDark : AppColors.saffronLight,
                    ),
                  ],
                ),

                // Allergen tags
                if (recipe.allergenTags.isNotEmpty) ...[
                  const SizedBox(height: AppSpacing.xl),
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.md),
                    decoration: BoxDecoration(
                      color: AppColors.warning.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(AppRadius.md),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const Icon(Icons.warning_amber_rounded, size: 18, color: AppColors.warning),
                            const SizedBox(width: 8),
                            Text(
                              'Diqqat — bu ovqatda:',
                              style: TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.w700,
                                color: AppColors.textDark,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Wrap(
                          spacing: 6,
                          runSpacing: 6,
                          children: recipe.allergenTags.map((t) {
                            return Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(AppRadius.pill),
                              ),
                              child: Text(
                                t.name,
                                style: const TextStyle(
                                  fontSize: 12,
                                  fontWeight: FontWeight.w500,
                                  color: AppColors.textDark,
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                ],

                // Ingredients
                const SizedBox(height: AppSpacing.xxl),
                _SectionTitle(title: 'Ingredientlar', count: recipe.ingredients.length),
                const SizedBox(height: AppSpacing.md),

                SectionCard(
                  color: Colors.white,
                  padding: EdgeInsets.zero,
                  child: Column(
                    children: [
                      for (int i = 0; i < recipe.ingredients.length; i++) ...[
                        _IngredientRow(ri: recipe.ingredients[i]),
                        if (i != recipe.ingredients.length - 1)
                          const Divider(height: 1, thickness: 0.5, indent: 56),
                      ],
                    ],
                  ),
                ),

                // Steps
                const SizedBox(height: AppSpacing.xxl),
                _SectionTitle(title: 'Tayyorlash', count: recipe.steps.length),
                const SizedBox(height: AppSpacing.md),

                for (final step in recipe.steps) ...[
                  _StepCard(step: step),
                  const SizedBox(height: AppSpacing.md),
                ],

                const SizedBox(height: AppSpacing.huge),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _BigBadge extends StatelessWidget {
  const _BigBadge({
    required this.icon,
    required this.value,
    required this.label,
    required this.color,
  });
  final IconData icon;
  final String value;
  final String label;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 78,
      padding: const EdgeInsets.symmetric(vertical: 12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(AppRadius.md),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 20),
          const SizedBox(height: 4),
          Text(
            value,
            style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: color),
          ),
          Text(
            label,
            style: const TextStyle(fontSize: 10, color: AppColors.textMedium),
          ),
        ],
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle({required this.title, required this.count});
  final String title;
  final int count;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(child: DisplayTitle(title, size: 20)),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: AppColors.creamCard,
            borderRadius: BorderRadius.circular(AppRadius.pill),
          ),
          child: Text(
            '$count',
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: AppColors.textDark),
          ),
        ),
      ],
    );
  }
}

class _IngredientRow extends StatelessWidget {
  const _IngredientRow({required this.ri});
  final RecipeIngredient ri;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: AppSpacing.md),
      child: Row(
        children: [
          FoodImage(
            imageUrl: ri.ingredient.imageUrl,
            emoji: _categoryEmoji(ri.ingredient.category),
            size: 36,
            radius: AppRadius.sm,
            background: AppColors.creamBg,
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Text(
              ri.ingredient.name,
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500, color: AppColors.textDark),
            ),
          ),
          Text(
            '${ri.amount} ${ri.unit}',
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w700,
              color: AppColors.terracotta,
            ),
          ),
        ],
      ),
    );
  }

  String _categoryEmoji(String category) {
    switch (category) {
      case 'VEGETABLE': return '🥬';
      case 'FRUIT': return '🍎';
      case 'MEAT': return '🥩';
      case 'DAIRY': return '🥛';
      case 'GRAIN': return '🌾';
      case 'SPICE': return '🌶️';
      case 'OIL': return '🫒';
      default: return '📦';
    }
  }
}

class _StepCard extends StatelessWidget {
  const _StepCard({required this.step});
  final RecipeStep step;

  @override
  Widget build(BuildContext context) {
    return SectionCard(
      color: Colors.white,
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 32, height: 32,
            decoration: const BoxDecoration(
              color: AppColors.terracotta,
              shape: BoxShape.circle,
            ),
            alignment: Alignment.center,
            child: Text(
              '${step.order}',
              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w700),
            ),
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Text(
              step.description,
              style: const TextStyle(fontSize: 14, height: 1.5, color: AppColors.textDark),
            ),
          ),
        ],
      ),
    );
  }
}
