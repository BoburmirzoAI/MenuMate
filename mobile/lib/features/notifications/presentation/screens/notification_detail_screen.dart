import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/section_card.dart';
import '../../data/notifications_repository.dart';

/// Bitta bildiruv to'liq — katta rasm, sarlavha, to'liq tanasi.
class NotificationDetailScreen extends ConsumerWidget {
  const NotificationDetailScreen({super.key, required this.id});
  final int id;

  static const _kindMeta = {
    'MENU': ('🍽️', Color(0xFFB84C3A), 'Menyu'),
    'HOLIDAY': ('🎉', Color(0xFFE0A93A), 'Bayram'),
    'ALLERGY': ('⚠️', Color(0xFFE07B4B), 'Ogohlantirish'),
    'UPDATE': ('🔔', Color(0xFF89A9C4), 'Yangilanish'),
    'GENERAL': ('📩', Color(0xFF7BA05B), 'Umumiy'),
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notifsAsync = ref.watch(notificationsListProvider);
    final notif = notifsAsync.value?.where((n) => n.id == id).firstOrNull;

    if (notif == null) {
      return Scaffold(
        appBar: AppBar(),
        body: notifsAsync.isLoading
            ? const Center(child: CircularProgressIndicator())
            : const Center(child: Text('Bildiruv topilmadi')),
      );
    }

    final meta = _kindMeta[notif.kind] ?? ('📩', AppColors.textLight, notif.kind);
    final whenExact =
        DateFormat("d MMMM yyyy · HH:mm", 'uz').format(notif.createdAt.toLocal());

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          // Rasm ustidagi appbar
          SliverAppBar(
            expandedHeight: notif.hasImage ? 260 : 0,
            pinned: true,
            backgroundColor: AppColors.creamBg,
            foregroundColor: AppColors.textDark,
            flexibleSpace: notif.hasImage
                ? FlexibleSpaceBar(
                    background: Stack(
                      fit: StackFit.expand,
                      children: [
                        Image.network(
                          notif.imageUrl,
                          fit: BoxFit.cover,
                          errorBuilder: (_, _, _) => Container(
                            color: AppColors.creamCard,
                            alignment: Alignment.center,
                            child: const Icon(Icons.image_not_supported,
                                size: 48, color: AppColors.textLight),
                          ),
                        ),
                        // Pastdan qorong'i gradient (o'qib bo'lish uchun)
                        Positioned(
                          left: 0, right: 0, bottom: 0, height: 80,
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
                      ],
                    ),
                  )
                : null,
          ),

          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.xxl),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: meta.$2,
                          borderRadius: BorderRadius.circular(AppRadius.pill),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(meta.$1, style: const TextStyle(fontSize: 12)),
                            const SizedBox(width: 4),
                            Text(
                              meta.$3,
                              style: const TextStyle(
                                fontSize: 11, fontWeight: FontWeight.w700,
                                color: Colors.white, letterSpacing: 0.4,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        whenExact,
                        style: TextStyle(
                          fontSize: 12, color: AppColors.textLight,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: AppSpacing.md),
                  DisplayTitle(notif.title, size: 26),
                  const SizedBox(height: AppSpacing.lg),
                  Text(
                    notif.body,
                    style: const TextStyle(
                      fontSize: 15, height: 1.55, color: AppColors.textDark,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.huge),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
