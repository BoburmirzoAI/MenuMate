import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/api/simple_repositories.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/router/app_routes.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/food_image.dart';
import '../../../../core/widgets/section_card.dart';
import '../../../auth/presentation/providers/auth_state.dart';
import '../../../family/data/family_repository.dart';
import '../../data/menu_repository.dart';
import '../../domain/menu.dart';

/// Bosh sahifa — mockup uslubida:
///  - Katta terracotta hero (oila nomi + salom + ob-havo qatori + bildiruv)
///  - "Bugungi menyu" 3 mahal kartochkasi ("HOZIR" badge bilan)
///  - Qora rangdagi "Xarid ro'yxati tayyor" banner
///  - 3 stat kartochka (a'zolar / kunlar / yaqin bayram)
class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authProvider).value;
    final user = (auth is AuthAuthenticated) ? auth.user : null;
    final familyAsync = ref.watch(myFamilyProvider);
    final membersAsync = ref.watch(familyMembersProvider);
    final menuAsync = ref.watch(currentMenuProvider);
    final weatherAsync = ref.watch(weatherProvider);

    final family = familyAsync.value;
    final members = membersAsync.value ?? const [];
    final menu = menuAsync.value;
    final weather = weatherAsync.value;

    return Scaffold(
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(currentMenuProvider);
          ref.invalidate(weatherProvider);
          ref.invalidate(myFamilyProvider);
          ref.invalidate(familyMembersProvider);
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _HeroCard(
                userName: user?.firstName ?? ref.tr('user'),
                familyName: family?.familyName ?? '',
                weather: weather,
                onTapProfile: () => context.push(AppRoutes.profile),
                onTapNotifications: () => context.push(AppRoutes.notifications),
              ),
              const SizedBox(height: AppSpacing.xl),

              Padding(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _SectionHeader(
                      title: ref.tr('dashboard_today_menu'),
                      trailingLabel: ref.tr('all'),
                      onTapTrailing: () => context.go(AppRoutes.menuList),
                    ),
                    const SizedBox(height: AppSpacing.md),
                    if (menuAsync.isLoading)
                      const _TodayMealsSkeleton()
                    else if (menu == null || menu.today == null)
                      _NoMenuCta(onCreate: () => _createMenu(context, ref))
                    else
                      _TodayMeals(day: menu.today!, menuId: menu.id),

                    const SizedBox(height: AppSpacing.xl),

                    if (menu != null) _ShoppingBanner(menu: menu),

                    const SizedBox(height: AppSpacing.xl),

                    _QuickStats(
                      membersCount: members.length,
                      daysInMenu: menu?.days.length ?? 0,
                    ),

                    const SizedBox(height: AppSpacing.huge),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _createMenu(BuildContext context, WidgetRef ref) async {
    try {
      await ref.read(menuRepositoryProvider).createMenu(
            startDate: DateTime.now(),
            duration: 'WEEKLY',
          );
      ref.invalidate(currentMenuProvider);
      if (context.mounted) context.go(AppRoutes.menuList);
    } on ApiException catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
    }
  }
}

// ============================================================================
// Hero card (terracotta)
// ============================================================================

class _HeroCard extends ConsumerWidget {
  const _HeroCard({
    required this.userName,
    required this.familyName,
    required this.weather,
    required this.onTapProfile,
    required this.onTapNotifications,
  });

  final String userName;
  final String familyName;
  final Weather? weather;
  final VoidCallback onTapProfile;
  final VoidCallback onTapNotifications;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.only(
        top: MediaQuery.paddingOf(context).top + AppSpacing.md,
        left: AppSpacing.xxl,
        right: AppSpacing.xxl,
        bottom: AppSpacing.xl,
      ),
      decoration: const BoxDecoration(
        color: AppColors.terracotta,
        borderRadius: BorderRadius.vertical(bottom: Radius.circular(28)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (familyName.isNotEmpty)
                      Text(
                        '$familyName ${ref.tr('dashboard_family_suffix')}',
                        style: TextStyle(
                          fontSize: 13,
                          color: Colors.white.withValues(alpha: 0.75),
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    const SizedBox(height: 6),
                    Text(
                      ref.tr('dashboard_greeting'),
                      style: TextStyle(
                        fontSize: 22, color: Colors.white.withValues(alpha: 0.9),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    Text(
                      '$userName!',
                      style: const TextStyle(
                        fontSize: 26, color: Colors.white, fontWeight: FontWeight.w700,
                        fontFamily: 'Fraunces',
                      ),
                    ),
                  ],
                ),
              ),
              _RoundIconButton(
                icon: Icons.notifications_outlined,
                showDot: true,
                onTap: onTapNotifications,
              ),
              const SizedBox(width: 8),
              _HeroAvatar(name: userName, onTap: onTapProfile),
            ],
          ),

          if (weather != null) ...[
            const SizedBox(height: AppSpacing.xl),
            Row(
              children: [
                Text(weather!.emoji, style: const TextStyle(fontSize: 18)),
                const SizedBox(width: 6),
                Text(weather!.city, style: _weatherStyle),
                _weatherDot,
                Text(
                  '${weather!.temperature.round()}° ${weather!.description}',
                  style: _weatherStyle,
                ),
              ],
            ),
          ],
        ],
      ),
    );
  }

  static const _weatherStyle = TextStyle(
    fontSize: 13, color: Colors.white, fontWeight: FontWeight.w500,
  );

  Widget get _weatherDot => const Padding(
        padding: EdgeInsets.symmetric(horizontal: 8),
        child: Text('·', style: TextStyle(color: Colors.white, fontSize: 14)),
      );
}

class _HeroAvatar extends StatelessWidget {
  const _HeroAvatar({required this.name, required this.onTap});
  final String name;
  final VoidCallback onTap;

  String get _initials {
    final trimmed = name.trim();
    if (trimmed.isEmpty) return '?';
    final parts = trimmed.split(RegExp(r'\s+'));
    if (parts.length == 1) return parts.first.characters.first.toUpperCase();
    return (parts.first.characters.first + parts.last.characters.first).toUpperCase();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 44, height: 44,
        decoration: BoxDecoration(
          color: Colors.white,
          shape: BoxShape.circle,
          border: Border.all(color: Colors.white.withValues(alpha: 0.5), width: 2),
        ),
        alignment: Alignment.center,
        child: Text(
          _initials,
          style: const TextStyle(
            color: AppColors.terracotta,
            fontSize: 16,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
    );
  }
}

class _RoundIconButton extends StatelessWidget {
  const _RoundIconButton({required this.icon, required this.onTap, this.showDot = false});
  final IconData icon;
  final VoidCallback onTap;
  final bool showDot;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Stack(
        clipBehavior: Clip.none,
        children: [
          Container(
            width: 44, height: 44,
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.2),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: Colors.white, size: 22),
          ),
          if (showDot)
            const Positioned(
              top: -1, right: -1,
              child: CircleAvatar(
                radius: 5, backgroundColor: AppColors.saffron,
              ),
            ),
        ],
      ),
    );
  }
}

// ============================================================================
// Section header
// ============================================================================

class _SectionHeader extends StatelessWidget {
  const _SectionHeader({
    required this.title,
    required this.trailingLabel,
    required this.onTapTrailing,
  });
  final String title;
  final String trailingLabel;
  final VoidCallback onTapTrailing;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(child: DisplayTitle(title, size: 22)),
        GestureDetector(
          onTap: onTapTrailing,
          child: Row(
            children: [
              Text(
                trailingLabel,
                style: const TextStyle(
                  fontSize: 13, fontWeight: FontWeight.w600, color: AppColors.terracotta,
                ),
              ),
              const SizedBox(width: 2),
              const Icon(Icons.arrow_forward, size: 14, color: AppColors.terracotta),
            ],
          ),
        ),
      ],
    );
  }
}

// ============================================================================
// Today meals
// ============================================================================

class _TodayMeals extends StatelessWidget {
  const _TodayMeals({required this.day, required this.menuId});
  final MenuDay day;
  final int menuId;

  static const _order = ['BREAKFAST', 'LUNCH', 'DINNER'];

  @override
  Widget build(BuildContext context) {
    final now = DateTime.now();
    final currentType = _currentMealType(now);

    final meals = _order
        .map((t) => day.mealFor(t))
        .whereType<MenuMeal>()
        .toList();

    return Column(
      children: [
        for (final meal in meals) ...[
          _MealTile(
            meal: meal,
            isCurrent: meal.mealType == currentType,
            onTap: () => context.push('/menu/$menuId/day/${day.id}'),
          ),
          const SizedBox(height: AppSpacing.md),
        ],
      ],
    );
  }

  String _currentMealType(DateTime now) {
    final h = now.hour;
    if (h < 11) return 'BREAKFAST';
    if (h < 16) return 'LUNCH';
    return 'DINNER';
  }
}

class _MealTile extends ConsumerWidget {
  const _MealTile({
    required this.meal,
    required this.isCurrent,
    required this.onTap,
  });
  final MenuMeal meal;
  final bool isCurrent;
  final VoidCallback onTap;

  static const _mealTimes = {
    'BREAKFAST': ('08:00', Color(0xFFE0A93A)),
    'LUNCH': ('13:00', Color(0xFFB84C3A)),
    'DINNER': ('19:00', Color(0xFF7BA05B)),
  };

  static const _mealLabelKeys = {
    'BREAKFAST': 'meal_breakfast',
    'LUNCH': 'meal_lunch',
    'DINNER': 'meal_dinner',
  };

  static const _emojis = {
    'BREAKFAST': '☕',
    'LUNCH': '🍲',
    'DINNER': '🍽️',
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final timeInfo = _mealTimes[meal.mealType] ?? ('00:00', AppColors.textLight);
    final label = ref.tr(_mealLabelKeys[meal.mealType] ?? 'meal').toUpperCase();
    final recipe = meal.mainRecipe;

    return Stack(
      clipBehavior: Clip.none,
      children: [
        Material(
          color: Colors.white,
          borderRadius: BorderRadius.circular(AppRadius.lg),
          child: InkWell(
            onTap: onTap,
            borderRadius: BorderRadius.circular(AppRadius.lg),
            child: Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(AppRadius.lg),
                border: isCurrent
                    ? Border.all(color: AppColors.terracotta, width: 2)
                    : null,
              ),
              padding: const EdgeInsets.all(AppSpacing.md),
              child: Row(
            children: [
              FoodImage(
                imageUrl: recipe?.imageUrl ?? '',
                emoji: _emojis[meal.mealType] ?? '🍴',
                size: 56,
                background: timeInfo.$2,
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '$label · ${timeInfo.$1}',
                      style: const TextStyle(
                        fontSize: 11, fontWeight: FontWeight.w700,
                        color: AppColors.textLight, letterSpacing: 0.7,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      recipe?.name ?? ref.tr('not_selected'),
                      style: TextStyle(
                        fontSize: 15, fontWeight: FontWeight.w700,
                        color: recipe != null ? AppColors.textDark : AppColors.textLight,
                        fontStyle: recipe != null ? FontStyle.normal : FontStyle.italic,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    if (recipe != null) ...[
                      const SizedBox(height: 2),
                      Text(
                        '${recipe.caloriesPerServing} ${ref.tr('kcal')} · ${recipe.prepTimeMinutes} ${ref.tr('min_short')}',
                        style: const TextStyle(fontSize: 12, color: AppColors.textLight),
                      ),
                    ],
                  ],
                ),
              ),
                  const Icon(Icons.chevron_right, color: AppColors.textLight),
                ],
              ),
            ),
          ),
        ),
        if (isCurrent)
          Positioned(
            top: -8, left: 12,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: AppColors.terracotta,
                borderRadius: BorderRadius.circular(AppRadius.pill),
              ),
              child: Text(
                ref.tr('meal_now_badge'),
                style: const TextStyle(
                  fontSize: 10, fontWeight: FontWeight.w700, color: Colors.white,
                ),
              ),
            ),
          ),
      ],
    );
  }
}

class _TodayMealsSkeleton extends StatelessWidget {
  const _TodayMealsSkeleton();
  @override
  Widget build(BuildContext context) => Column(
        children: List.generate(3, (_) => Padding(
          padding: const EdgeInsets.only(bottom: AppSpacing.md),
          child: Container(
            height: 80,
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.5),
              borderRadius: BorderRadius.circular(AppRadius.lg),
            ),
          ),
        )),
      );
}

class _NoMenuCta extends ConsumerWidget {
  const _NoMenuCta({required this.onCreate});
  final VoidCallback onCreate;

  @override
  Widget build(BuildContext context, WidgetRef ref) => SectionCard(
        color: Colors.white,
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          children: [
            const Text('📅', style: TextStyle(fontSize: 40)),
            const SizedBox(height: AppSpacing.md),
            DisplayTitle(ref.tr('dashboard_no_menu_title'), size: 18),
            const SizedBox(height: 4),
            Text(
              ref.tr('dashboard_no_menu_subtitle'),
              style: TextStyle(color: AppColors.textMedium, fontSize: 13),
            ),
            const SizedBox(height: AppSpacing.lg),
            ElevatedButton.icon(
              onPressed: onCreate,
              icon: const Icon(Icons.add, size: 18),
              label: Text(ref.tr('dashboard_create_menu')),
            ),
          ],
        ),
      );
}

// ============================================================================
// Shopping list banner (qora)
// ============================================================================

class _ShoppingBanner extends ConsumerWidget {
  const _ShoppingBanner({required this.menu});
  final Menu menu;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final listAsync = ref.watch(shoppingListProvider(menu.id));
    final list = listAsync.value;
    final totalItems = list?.totalItems ?? 0;
    final categories = list?.itemsByCategory.length ?? 0;

    return GestureDetector(
      onTap: () => context.go(AppRoutes.shopping),
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.lg),
        decoration: BoxDecoration(
          color: const Color(0xFF2B1810),
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        child: Row(
          children: [
            const Text('🛒', style: TextStyle(fontSize: 26)),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    ref.tr('dashboard_shopping_ready_title'),
                    style: const TextStyle(
                      fontSize: 15, fontWeight: FontWeight.w700, color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    '$totalItems ${ref.tr('shopping_kgo_items_of')} · $categories',
                    style: TextStyle(
                      fontSize: 12, color: Colors.white.withValues(alpha: 0.7),
                    ),
                  ),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              decoration: BoxDecoration(
                color: AppColors.saffron,
                borderRadius: BorderRadius.circular(AppRadius.pill),
              ),
              child: Text(
                ref.tr('open'),
                style: const TextStyle(
                  fontSize: 13, fontWeight: FontWeight.w700, color: Colors.white,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================================
// Quick stats
// ============================================================================

class _QuickStats extends ConsumerWidget {
  const _QuickStats({required this.membersCount, required this.daysInMenu});
  final int membersCount;
  final int daysInMenu;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Row(
      children: [
        Expanded(
          child: _StatCard(
            emoji: '👨‍👩‍👧',
            title: '$membersCount ${ref.tr('dashboard_stat_members')}',
            onTap: () => context.push(AppRoutes.memberList),
          ),
        ),
        const SizedBox(width: AppSpacing.md),
        Expanded(
          child: _StatCard(
            emoji: '📅',
            title: '$daysInMenu ${ref.tr('dashboard_stat_days')}',
            onTap: () => context.go(AppRoutes.menuList),
          ),
        ),
        const SizedBox(width: AppSpacing.md),
        Expanded(
          child: _StatCard(
            emoji: '🎉',
            title: ref.tr('dashboard_stat_holiday'),
            onTap: () => context.push(AppRoutes.notifications),
          ),
        ),
      ],
    );
  }
}

class _StatCard extends StatelessWidget {
  const _StatCard({
    required this.emoji,
    required this.title,
    required this.onTap,
  });
  final String emoji;
  final String title;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Material(
        color: Colors.white,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(AppRadius.lg),
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
            child: Column(
              children: [
                Text(emoji, style: const TextStyle(fontSize: 26)),
                const SizedBox(height: 4),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textDark,
                  ),
                ),
              ],
            ),
          ),
        ),
      );
}
