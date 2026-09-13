import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/food_image.dart';
import '../../../../core/widgets/section_card.dart';
import '../../../../core/widgets/state_views.dart';
import '../../data/menu_repository.dart';
import '../../domain/menu.dart';

/// Menyu list — mockup uslubida timeline + stats + 7/30 kun toggle.
class MenuListScreen extends ConsumerWidget {
  const MenuListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final menuAsync = ref.watch(currentMenuProvider);

    return Scaffold(
      body: SafeArea(
        child: menuAsync.when(
          loading: () => const LoadingView(),
          error: (err, _) => ErrorRetryView(
            message: err is ApiException ? err.message : ref.tr('error'),
            onRetry: () => ref.invalidate(currentMenuProvider),
          ),
          data: (menu) => menu == null
              ? EmptyView(
                  emoji: '📅',
                  title: ref.tr('menu_empty_title'),
                  subtitle: ref.tr('menu_empty_subtitle'),
                  ctaLabel: ref.tr('dashboard_create_menu'),
                  onCta: () => _createMenu(context, ref, 'WEEKLY'),
                )
              : _MenuContent(
                  menu: menu,
                  onSwitchDuration: (d) => _createMenu(context, ref, d),
                ),
        ),
      ),
    );
  }

  Future<void> _createMenu(
    BuildContext context, WidgetRef ref, String duration,
  ) async {
    try {
      await ref.read(menuRepositoryProvider).createMenu(
            startDate: DateTime.now(),
            duration: duration,
          );
      ref.invalidate(currentMenuProvider);
    } on ApiException catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
    }
  }
}

class _MenuContent extends ConsumerWidget {
  const _MenuContent({required this.menu, required this.onSwitchDuration});
  final Menu menu;
  final ValueChanged<String> onSwitchDuration;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final statsAsync = ref.watch(_menuStatsProvider(menu.id));
    final today = DateTime.now();
    final periodLabel = menu.duration == 'MONTHLY'
        ? ref.tr('menu_this_month')
        : ref.tr('menu_this_week');

    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(
              AppSpacing.xxl, AppSpacing.lg, AppSpacing.xxl, AppSpacing.md,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            ref.tr('menu_your_title'),
                            style: TextStyle(color: AppColors.textMedium, fontSize: 13),
                          ),
                          const SizedBox(height: 2),
                          DisplayTitle(periodLabel, size: 30),
                        ],
                      ),
                    ),
                    _DurationToggle(
                      selected: menu.duration,
                      onSelect: (d) {
                        if (d != menu.duration) _confirmSwitch(context, ref, d);
                      },
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.xl),
                statsAsync.when(
                  loading: () => const _StatsRowSkeleton(),
                  error: (_, _) => const SizedBox.shrink(),
                  data: (s) => _StatsRow(
                    calories: (s['total_calories'] as int?) ?? 0,
                    recipes: (s['recipe_count'] as int?) ?? 0,
                    halalPercent: (s['halal_percent'] as int?) ?? 100,
                  ),
                ),
              ],
            ),
          ),
        ),
        SliverPadding(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
          sliver: SliverList.builder(
            itemCount: menu.days.length,
            itemBuilder: (context, i) => _TimelineRow(
              day: menu.days[i],
              isToday: _isSameDay(menu.days[i].date, today),
              isLast: i == menu.days.length - 1,
              menuId: menu.id,
            ),
          ),
        ),
        const SliverToBoxAdapter(child: SizedBox(height: AppSpacing.huge)),
      ],
    );
  }

  void _confirmSwitch(BuildContext context, WidgetRef ref, String newDuration) {
    final titleKey = newDuration == 'MONTHLY'
        ? 'menu_switch_dialog_title_30'
        : 'menu_switch_dialog_title_7';
    showDialog(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text(ref.tr(titleKey)),
        content: Text(ref.tr('menu_switch_dialog_body')),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(dialogContext).pop(),
            child: Text(ref.tr('cancel')),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(dialogContext).pop();
              onSwitchDuration(newDuration);
            },
            child: Text(ref.tr('add')),
          ),
        ],
      ),
    );
  }

  bool _isSameDay(DateTime a, DateTime b) =>
      a.year == b.year && a.month == b.month && a.day == b.day;
}

// ============================================================================
// Duration toggle (7 kun / 30 kun)
// ============================================================================

class _DurationToggle extends ConsumerWidget {
  const _DurationToggle({required this.selected, required this.onSelect});

  final String selected;
  final ValueChanged<String> onSelect;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      padding: const EdgeInsets.all(3),
      decoration: BoxDecoration(
        color: AppColors.creamCard,
        borderRadius: BorderRadius.circular(AppRadius.pill),
      ),
      child: Row(
        children: [
          _pill(ref.tr('menu_days_7'), 'WEEKLY'),
          _pill(ref.tr('menu_days_30'), 'MONTHLY'),
        ],
      ),
    );
  }

  Widget _pill(String label, String value) {
    final active = selected == value;
    return GestureDetector(
      onTap: () => onSelect(value),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        decoration: BoxDecoration(
          color: active ? AppColors.saffron : Colors.transparent,
          borderRadius: BorderRadius.circular(AppRadius.pill),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w700,
            color: active ? Colors.white : AppColors.textMedium,
          ),
        ),
      ),
    );
  }
}

// ============================================================================
// Stats row
// ============================================================================

class _StatsRow extends ConsumerWidget {
  const _StatsRow({
    required this.calories,
    required this.recipes,
    required this.halalPercent,
  });

  final int calories;
  final int recipes;
  final int halalPercent;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Row(
      children: [
        Expanded(child: _StatTile(
          label: ref.tr('menu_stat_calories').toUpperCase(),
          value: NumberFormat('#,###').format(calories),
        )),
        const SizedBox(width: AppSpacing.md),
        Expanded(child: _StatTile(
          label: ref.tr('menu_stat_recipes').toUpperCase(),
          value: '$recipes',
        )),
        const SizedBox(width: AppSpacing.md),
        Expanded(child: _StatTile(
          label: ref.tr('menu_stat_halal').toUpperCase(),
          value: '✓$halalPercent%',
          valueColor: AppColors.success,
        )),
      ],
    );
  }
}

class _StatTile extends StatelessWidget {
  const _StatTile({required this.label, required this.value, this.valueColor});
  final String label;
  final String value;
  final Color? valueColor;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        border: Border.all(color: AppColors.creamCard),
      ),
      child: Column(
        children: [
          Text(
            label,
            style: TextStyle(
              fontSize: 10, fontWeight: FontWeight.w700,
              letterSpacing: 1.2, color: AppColors.textLight,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            value,
            style: TextStyle(
              fontSize: 18, fontWeight: FontWeight.w700,
              color: valueColor ?? AppColors.terracotta,
            ),
          ),
        ],
      ),
    );
  }
}

class _StatsRowSkeleton extends StatelessWidget {
  const _StatsRowSkeleton();
  @override
  Widget build(BuildContext context) => SizedBox(
        height: 70,
        child: Row(
          children: List.generate(3, (i) => Expanded(
            child: Padding(
              padding: const EdgeInsets.only(right: AppSpacing.md),
              child: Container(
                decoration: BoxDecoration(
                  color: AppColors.creamCard.withValues(alpha: 0.6),
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                ),
              ),
            ),
          )),
        ),
      );
}

// ============================================================================
// Timeline row (raqamli circle + dashed chiziq + kun kartochkasi)
// ============================================================================

class _TimelineRow extends StatelessWidget {
  const _TimelineRow({
    required this.day,
    required this.isToday,
    required this.isLast,
    required this.menuId,
  });

  final MenuDay day;
  final bool isToday;
  final bool isLast;
  final int menuId;

  @override
  Widget build(BuildContext context) {
    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _TimelineNode(day: day.date.day, isToday: isToday, isHoliday: day.isHoliday, isLast: isLast),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(bottom: AppSpacing.md),
              child: _DayCard(day: day, isToday: isToday, menuId: menuId),
            ),
          ),
        ],
      ),
    );
  }
}

class _TimelineNode extends StatelessWidget {
  const _TimelineNode({
    required this.day,
    required this.isToday,
    required this.isHoliday,
    required this.isLast,
  });

  final int day;
  final bool isToday;
  final bool isHoliday;
  final bool isLast;

  @override
  Widget build(BuildContext context) {
    final Color bg;
    final Color fg;
    final Color border;
    if (isToday) {
      bg = AppColors.terracotta;
      fg = Colors.white;
      border = AppColors.terracotta;
    } else if (isHoliday) {
      bg = AppColors.saffron;
      fg = Colors.white;
      border = AppColors.saffron;
    } else {
      bg = Colors.white;
      fg = AppColors.textDark;
      border = AppColors.creamAccent;
    }
    return SizedBox(
      width: 32,
      child: Column(
        children: [
          Container(
            width: 32, height: 32,
            decoration: BoxDecoration(
              color: bg,
              shape: BoxShape.circle,
              border: Border.all(color: border, width: 1.5),
            ),
            alignment: Alignment.center,
            child: Text(
              '$day',
              style: TextStyle(
                fontSize: 13, fontWeight: FontWeight.w700, color: fg,
              ),
            ),
          ),
          if (!isLast)
            Expanded(
              child: CustomPaint(
                painter: _DashedLinePainter(),
                child: const SizedBox(width: 2),
              ),
            ),
        ],
      ),
    );
  }
}

class _DashedLinePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppColors.creamAccent
      ..strokeWidth = 1.5;
    const dash = 4.0, gap = 4.0;
    double y = 0;
    final x = size.width / 2;
    while (y < size.height) {
      canvas.drawLine(Offset(x, y), Offset(x, (y + dash).clamp(0, size.height)), paint);
      y += dash + gap;
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

// ============================================================================
// Day card
// ============================================================================

class _DayCard extends ConsumerWidget {
  const _DayCard({required this.day, required this.isToday, required this.menuId});

  final MenuDay day;
  final bool isToday;
  final int menuId;

  static const _mealEmojis = {
    'BREAKFAST': '☕',
    'LUNCH': '🍲',
    'DINNER': '🍽️',
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dayName = DateFormat('EEEE', 'uz').format(day.date).toUpperCase();
    final b = day.mealFor('BREAKFAST');
    final l = day.mealFor('LUNCH');
    final d = day.mealFor('DINNER');

    return SectionCard(
      onTap: () => context.push('/menu/$menuId/day/${day.id}'),
      color: day.isHoliday
          ? AppColors.creamAccent
          : (isToday ? AppColors.creamCard : Colors.white),
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  dayName,
                  style: const TextStyle(
                    fontSize: 12, fontWeight: FontWeight.w700,
                    color: AppColors.textMedium, letterSpacing: 0.8,
                  ),
                ),
              ),
              if (isToday) _StatusBadge(label: ref.tr('menu_status_today'), color: AppColors.terracotta),
              if (!isToday && day.isHoliday)
                _StatusBadge(label: day.holidayName.toUpperCase(), color: AppColors.saffronLight),
              if (!isToday && !day.isHoliday)
                _StatusBadge(label: ref.tr('menu_status_active'), color: AppColors.success),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          Row(
            children: [
              _MealPreview(
                emoji: _mealEmojis['BREAKFAST']!,
                name: b?.mainRecipe?.name,
                imageUrl: b?.mainRecipe?.imageUrl ?? '',
              ),
              const SizedBox(width: 8),
              _MealPreview(
                emoji: _mealEmojis['LUNCH']!,
                name: l?.mainRecipe?.name,
                imageUrl: l?.mainRecipe?.imageUrl ?? '',
              ),
              const SizedBox(width: 8),
              _MealPreview(
                emoji: _mealEmojis['DINNER']!,
                name: d?.mainRecipe?.name,
                imageUrl: d?.mainRecipe?.imageUrl ?? '',
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _StatusBadge extends StatelessWidget {
  const _StatusBadge({required this.label, required this.color});
  final String label;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(AppRadius.pill),
      ),
      child: Text(
        label,
        style: const TextStyle(
          fontSize: 10, fontWeight: FontWeight.w700,
          color: Colors.white, letterSpacing: 0.6,
        ),
      ),
    );
  }
}

class _MealPreview extends StatelessWidget {
  const _MealPreview({
    required this.emoji,
    required this.name,
    required this.imageUrl,
  });
  final String emoji;
  final String? name;
  final String imageUrl;

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        children: [
          FoodImage(
            imageUrl: imageUrl,
            emoji: emoji,
            size: 42,
            radius: AppRadius.sm,
            background: AppColors.creamCard,
          ),
          const SizedBox(height: 4),
          Text(
            name ?? '—',
            maxLines: 2,
            textAlign: TextAlign.center,
            overflow: TextOverflow.ellipsis,
            style: TextStyle(
              fontSize: 11,
              color: name != null ? AppColors.textDark : AppColors.textLight,
              fontWeight: FontWeight.w600,
              fontStyle: name != null ? FontStyle.normal : FontStyle.italic,
            ),
          ),
        ],
      ),
    );
  }
}

// ============================================================================
// Empty & error
// ============================================================================


// ============================================================================
// Stats provider
// ============================================================================

final _menuStatsProvider =
    FutureProvider.autoDispose.family<Map<String, dynamic>, int>((ref, menuId) async {
  return ref.watch(menuRepositoryProvider).getStats(menuId);
});
