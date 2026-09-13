import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/section_card.dart';
import '../../data/notifications_repository.dart';
import '../../domain/notification.dart';

class NotificationsScreen extends ConsumerWidget {
  const NotificationsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notifsAsync = ref.watch(notificationsListProvider);
    final holidaysAsync = ref.watch(upcomingHolidaysProvider);
    final unread = notifsAsync.value?.where((n) => !n.isRead).length ?? 0;

    return Scaffold(
      appBar: AppBar(
        title: Text(ref.tr('notifications_title')),
        centerTitle: false,
        actions: [
          if (unread > 0)
            TextButton.icon(
              onPressed: () => _markAllRead(context, ref),
              icon: const Icon(Icons.done_all, size: 18),
              label: Text(ref.tr('notifications_all_read')),
            ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(notificationsListProvider);
          ref.invalidate(upcomingHolidaysProvider);
        },
        child: ListView(
          padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
          physics: const AlwaysScrollableScrollPhysics(),
          children: [
            // Yaqin bayramlar
            Padding(
              padding: const EdgeInsets.fromLTRB(
                AppSpacing.xxl, AppSpacing.sm, AppSpacing.xxl, AppSpacing.sm,
              ),
              child: _SectionTitle(ref.tr('notifications_upcoming_holidays')),
            ),
            holidaysAsync.when(
              loading: () => const _HolidaySkeleton(),
              error: (_, _) => const SizedBox.shrink(),
              data: (list) {
                if (list.isEmpty) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
                    child: _MutedRow(
                      icon: Icons.event_available,
                      text: ref.tr('notifications_no_holidays'),
                    ),
                  );
                }
                return SizedBox(
                  height: 138,
                  child: ListView.separated(
                    scrollDirection: Axis.horizontal,
                    padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
                    itemCount: list.length,
                    separatorBuilder: (_, _) => const SizedBox(width: AppSpacing.md),
                    itemBuilder: (context, i) => _HolidayCard(holiday: list[i]),
                  ),
                );
              },
            ),

            const SizedBox(height: AppSpacing.xxl),

            // Bildiruvlar
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
              child: Row(
                children: [
                  Expanded(child: _SectionTitle(ref.tr('notifications_section'))),
                  if (unread > 0)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                      decoration: BoxDecoration(
                        color: AppColors.terracotta,
                        borderRadius: BorderRadius.circular(AppRadius.pill),
                      ),
                      child: Text(
                        '$unread ${ref.tr('notifications_new_count_suffix')}',
                        style: const TextStyle(
                          fontSize: 11, fontWeight: FontWeight.w700, color: Colors.white,
                        ),
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.sm),
            notifsAsync.when(
              loading: () => const Padding(
                padding: EdgeInsets.all(AppSpacing.xl),
                child: Center(child: CircularProgressIndicator()),
              ),
              error: (err, _) => Padding(
                padding: const EdgeInsets.all(AppSpacing.xl),
                child: Text(
                  err is ApiException ? err.message : ref.tr('error'),
                  style: const TextStyle(color: AppColors.error),
                ),
              ),
              data: (notifs) {
                if (notifs.isEmpty) return const _EmptyNotifs();
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
                  child: Column(
                    children: [
                      for (final n in notifs) ...[
                        _NotificationCard(
                          notif: n,
                          onTap: () => _openNotification(context, ref, n),
                        ),
                        const SizedBox(height: AppSpacing.md),
                      ],
                    ],
                  ),
                );
              },
            ),

            const SizedBox(height: AppSpacing.huge),
          ],
        ),
      ),
    );
  }

  Future<void> _markAllRead(BuildContext context, WidgetRef ref) async {
    try {
      await ref.read(notificationsRepositoryProvider).markAllRead();
      ref.invalidate(notificationsListProvider);
    } on ApiException catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
    }
  }

  Future<void> _openNotification(
    BuildContext context, WidgetRef ref, AppNotification n,
  ) async {
    // Detail ekranni ochamiz
    await context.push('/notifications/${n.id}');
    // Qaytganda o'qilgan qilamiz
    if (!n.isRead) {
      try {
        await ref.read(notificationsRepositoryProvider).markRead(n.id);
        ref.invalidate(notificationsListProvider);
      } on ApiException {
        // jimgina
      }
    }
  }
}

// ============================================================================
// Holiday card (rasm bilan)
// ============================================================================

class _HolidayCard extends ConsumerWidget {
  const _HolidayCard({required this.holiday});
  final UpcomingHoliday holiday;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dateLabel = DateFormat('d MMM', 'uz').format(holiday.upcomingDate);
    return Container(
      width: 220,
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFFF5B841), Color(0xFFE0A93A)],
          begin: Alignment.topLeft, end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(AppRadius.lg),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Text('🎉', style: TextStyle(fontSize: 26)),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(AppRadius.pill),
                ),
                child: Text(
                  '${holiday.daysUntil} ${ref.tr('days_short')}',
                  style: const TextStyle(
                    fontSize: 11, fontWeight: FontWeight.w700,
                    color: AppColors.terracotta,
                  ),
                ),
              ),
            ],
          ),
          const Spacer(),
          Text(
            holiday.name,
            style: const TextStyle(
              fontSize: 14, fontWeight: FontWeight.w700,
              color: Colors.white, height: 1.25,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 4),
          Row(
            children: [
              const Icon(Icons.calendar_month, size: 12, color: Colors.white),
              const SizedBox(width: 4),
              Text(
                dateLabel,
                style: const TextStyle(
                  fontSize: 11, color: Colors.white, fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _HolidaySkeleton extends StatelessWidget {
  const _HolidaySkeleton();
  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
        child: Container(
          height: 138,
          decoration: BoxDecoration(
            color: AppColors.creamCard,
            borderRadius: BorderRadius.circular(AppRadius.lg),
          ),
        ),
      );
}

// ============================================================================
// Notification card (rasm + katta kartochka)
// ============================================================================

class _NotificationCard extends ConsumerWidget {
  const _NotificationCard({required this.notif, required this.onTap});
  final AppNotification notif;
  final VoidCallback onTap;

  static const _kindEmoji = {
    'MENU': ('🍽️', Color(0xFFB84C3A), 'notif_kind_menu'),
    'HOLIDAY': ('🎉', Color(0xFFE0A93A), 'notif_kind_holiday'),
    'ALLERGY': ('⚠️', Color(0xFFE07B4B), 'notif_kind_allergy'),
    'UPDATE': ('🔔', Color(0xFF89A9C4), 'notif_kind_update'),
    'GENERAL': ('📩', Color(0xFF7BA05B), 'notif_kind_general'),
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final metaTuple = _kindEmoji[notif.kind] ?? ('📩', AppColors.textLight, 'notif_kind_general');
    final meta = (metaTuple.$1, metaTuple.$2, ref.tr(metaTuple.$3));
    final when = _formatWhen(context, ref, notif.createdAt);

    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(AppRadius.lg),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        child: Stack(
          children: [
            // Chap tomonda rangli chiziq — o'qilmagan bo'lsa
            if (!notif.isRead)
              Positioned(
                left: 0, top: 12, bottom: 12,
                child: Container(
                  width: 4,
                  decoration: BoxDecoration(
                    color: meta.$2,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
            Padding(
              padding: const EdgeInsets.all(AppSpacing.md),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Kind ikon
                  Container(
                    width: 44, height: 44,
                    decoration: BoxDecoration(
                      color: meta.$2.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(AppRadius.md),
                    ),
                    alignment: Alignment.center,
                    child: Text(meta.$1, style: const TextStyle(fontSize: 22)),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: meta.$2.withValues(alpha: 0.15),
                                borderRadius: BorderRadius.circular(AppRadius.sm),
                              ),
                              child: Text(
                                meta.$3.toUpperCase(),
                                style: TextStyle(
                                  fontSize: 9,
                                  fontWeight: FontWeight.w700,
                                  color: meta.$2,
                                  letterSpacing: 0.5,
                                ),
                              ),
                            ),
                            const Spacer(),
                            Text(
                              when,
                              style: const TextStyle(
                                fontSize: 11, color: AppColors.textLight,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        Text(
                          notif.title,
                          style: TextStyle(
                            fontSize: 15,
                            fontWeight: notif.isRead ? FontWeight.w600 : FontWeight.w700,
                            color: AppColors.textDark,
                            height: 1.25,
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 4),
                        Text(
                          notif.body,
                          style: TextStyle(
                            fontSize: 13,
                            color: notif.isRead ? AppColors.textLight : AppColors.textMedium,
                            height: 1.35,
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                  if (notif.hasImage) ...[
                    const SizedBox(width: AppSpacing.md),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(AppRadius.md),
                      child: Image.network(
                        notif.imageUrl,
                        width: 68, height: 68, fit: BoxFit.cover,
                        errorBuilder: (_, _, _) => Container(
                          width: 68, height: 68,
                          color: AppColors.creamCard,
                          child: const Icon(Icons.image_not_supported,
                              color: AppColors.textLight),
                        ),
                        loadingBuilder: (_, child, prog) => prog == null
                            ? child
                            : Container(
                                width: 68, height: 68, color: AppColors.creamCard,
                              ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _formatWhen(BuildContext context, WidgetRef ref, DateTime dt) {
    final now = DateTime.now();
    final diff = now.difference(dt);
    if (diff.inMinutes < 1) return ref.tr('time_just_now');
    if (diff.inMinutes < 60) return "${diff.inMinutes} ${ref.tr('time_min_ago')}";
    if (diff.inHours < 24) return "${diff.inHours} ${ref.tr('time_hour_ago')}";
    if (diff.inDays < 7) return "${diff.inDays} ${ref.tr('time_day_ago')}";
    return DateFormat('d MMM', 'uz').format(dt);
  }
}

// ============================================================================
// Muted row & empty state
// ============================================================================

class _EmptyNotifs extends ConsumerWidget {
  const _EmptyNotifs();
  @override
  Widget build(BuildContext context, WidgetRef ref) => Padding(
        padding: const EdgeInsets.all(AppSpacing.xxxl),
        child: Column(
          children: [
            const Text('🔔', style: TextStyle(fontSize: 48)),
            const SizedBox(height: AppSpacing.md),
            DisplayTitle(ref.tr('notifications_empty_title'), size: 18),
            const SizedBox(height: 4),
            Text(
              ref.tr('notifications_empty_body'),
              textAlign: TextAlign.center,
              style: TextStyle(color: AppColors.textMedium, fontSize: 13),
            ),
          ],
        ),
      );
}

class _MutedRow extends StatelessWidget {
  const _MutedRow({required this.icon, required this.text});
  final IconData icon;
  final String text;
  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.all(AppSpacing.lg),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        child: Row(
          children: [
            Icon(icon, color: AppColors.textLight, size: 20),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Text(text, style: TextStyle(color: AppColors.textMedium)),
            ),
          ],
        ),
      );
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.title);
  final String title;
  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(left: 4),
        child: Text(
          title.toUpperCase(),
          style: const TextStyle(
            fontSize: 11, fontWeight: FontWeight.w700,
            color: AppColors.textLight, letterSpacing: 0.8,
          ),
        ),
      );
}
