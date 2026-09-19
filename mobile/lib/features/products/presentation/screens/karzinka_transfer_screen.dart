import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../../../core/api/simple_repositories.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/food_image.dart';
import '../../../../core/widgets/section_card.dart';
import '../../../../core/widgets/state_views.dart';
import '../../../menu/data/menu_repository.dart';
import '../../state/shopping_checks_provider.dart';

/// Xarid ro'yxatidan tanlangan mahsulotlarni Karzinka Go ilovasiga o'tkazish.
class KarzinkaTransferScreen extends ConsumerWidget {
  const KarzinkaTransferScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final menu = ref.watch(currentMenuProvider).value;
    final listAsync = menu == null
        ? const AsyncValue<ShoppingList?>.data(null)
        : ref.watch(shoppingListProvider(menu.id));

    return Scaffold(
      appBar: AppBar(
        title: Text(ref.tr('shopping_transfer_cta')),
        centerTitle: false,
      ),
      body: listAsync.when(
        loading: () => const LoadingView(),
        error: (err, _) => ErrorRetryView(
          message: '$err',
          onRetry: () => menu == null ? null : ref.invalidate(shoppingListProvider(menu.id)),
        ),
        data: (list) {
          if (list == null || list.totalItems == 0) {
            return EmptyView(
              emoji: '🛒',
              title: ref.tr('shopping_empty_body'),
            );
          }
          return _Content(list: list);
        },
      ),
    );
  }
}

class _Content extends ConsumerWidget {
  const _Content({required this.list});
  final ShoppingList list;

  // Karzinka Go identifikatorlari. Deep-link scheme rasman e'lon qilinmagan,
  // shuning uchun Android'da package name orqali intent qilamiz, iOS'da esa
  // to'g'ridan App Store'ga (o'sha yerda "Open" tugmasi ilovani ochadi).
  static const _karzinkaPackageName = 'com.korzinka.go';
  static const _karzinkaAppStoreId = '1671724827';
  static const _karzinkaWebUrl = 'https://korzinka.uz/go';

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Faqat Karzinka'da mavjud va tanlangan mahsulotlar
    final localChecks = ref.watch(shoppingLocalChecksProvider);
    final available = <ShoppingItem>[];
    for (final items in list.itemsByCategory.values) {
      for (final it in items) {
        final checked = localChecks[it.id] ?? it.isPurchased;
        if (checked && it.kgoAvailable && it.kgoProductUrl.isNotEmpty) {
          available.add(it);
        }
      }
    }

    final total = available.fold<double>(
      0,
      (sum, it) => sum + (double.tryParse(it.priceTotal ?? '') ?? 0),
    );

    if (available.isEmpty) {
      return EmptyView(
        emoji: '🛒',
        title: ref.tr('shopping_no_selection'),
        subtitle: ref.tr('karzinka_transfer_empty_body'),
      );
    }

    return Column(
      children: [
        Expanded(
          child: ListView(
            padding: const EdgeInsets.all(AppSpacing.xxl),
            children: [
              // Banner
              Container(
                padding: const EdgeInsets.all(AppSpacing.lg),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF4A2E1F), Color(0xFF3A2417)],
                    begin: Alignment.centerLeft, end: Alignment.centerRight,
                  ),
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 44, height: 44,
                      decoration: BoxDecoration(
                        color: AppColors.saffron,
                        borderRadius: BorderRadius.circular(AppRadius.md),
                      ),
                      alignment: Alignment.center,
                      child: const Icon(Icons.shopping_bag_outlined, color: Colors.white),
                    ),
                    const SizedBox(width: AppSpacing.md),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '${available.length} ${ref.tr('shopping_kgo_items_of')}',
                            style: const TextStyle(
                              color: Colors.white, fontSize: 14, fontWeight: FontWeight.w700,
                            ),
                          ),
                          Text(
                            '${NumberFormat('#,###', 'ru').format(total)} ${ref.tr('som')}',
                            style: const TextStyle(
                              color: AppColors.saffron, fontSize: 12, fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.lg),

              // Katta CTA
              ElevatedButton.icon(
                onPressed: () => _openAppMain(context, ref),
                icon: const Icon(Icons.open_in_new, size: 20),
                label: Text(ref.tr('karzinka_open_app')),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.saffron,
                  foregroundColor: Colors.white,
                  minimumSize: const Size.fromHeight(52),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.lg)),
                ),
              ),
              const SizedBox(height: AppSpacing.lg),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
                child: Text(
                  ref.tr('karzinka_or_tap_each'),
                  textAlign: TextAlign.center,
                  style: TextStyle(color: AppColors.textLight, fontSize: 12),
                ),
              ),
              const SizedBox(height: AppSpacing.md),

              // Mahsulot ro'yxati — har biri o'z linkiga ega
              for (final it in available) _ProductRow(item: it),

              const SizedBox(height: AppSpacing.huge),
            ],
          ),
        ),
      ],
    );
  }

  Future<void> _openAppMain(BuildContext context, WidgetRef ref) async {
    if (Platform.isAndroid) {
      final intentUri = Uri.parse(
        'intent://open/#Intent;package=$_karzinkaPackageName;end;',
      );
      try {
        if (await launchUrl(intentUri, mode: LaunchMode.externalApplication)) {
          return;
        }
      } catch (_) {}

      final market = Uri.parse('market://details?id=$_karzinkaPackageName');
      try {
        if (await launchUrl(market, mode: LaunchMode.externalApplication)) {
          return;
        }
      } catch (_) {}

      final playStoreWeb = Uri.parse(
        'https://play.google.com/store/apps/details?id=$_karzinkaPackageName',
      );
      if (await launchUrl(playStoreWeb, mode: LaunchMode.externalApplication)) {
        return;
      }
    } else if (Platform.isIOS) {
      final appStore = Uri.parse(
        'https://apps.apple.com/uz/app/id$_karzinkaAppStoreId',
      );
      if (await launchUrl(appStore, mode: LaunchMode.externalApplication)) {
        return;
      }
    } else {
      final web = Uri.parse(_karzinkaWebUrl);
      if (await launchUrl(web, mode: LaunchMode.externalApplication)) {
        return;
      }
    }

    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(ref.tr('karzinka_open_failed'))),
      );
    }
  }
}

class _ProductRow extends ConsumerWidget {
  const _ProductRow({required this.item});
  final ShoppingItem item;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.md),
      child: SectionCard(
        color: Colors.white,
        padding: const EdgeInsets.all(AppSpacing.md),
        onTap: () => _openProduct(context, ref),
        child: Row(
          children: [
            FoodImage(
              imageUrl: item.kgoImageUrl.isNotEmpty
                  ? item.kgoImageUrl
                  : item.ingredientImageUrl,
              emoji: '📦',
              size: 52,
              radius: AppRadius.sm,
              background: AppColors.creamCard,
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    item.kgoTitle.isNotEmpty ? item.kgoTitle : item.ingredientName,
                    style: const TextStyle(
                      fontSize: 14, fontWeight: FontWeight.w700, color: AppColors.textDark,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  if (item.kgoWeight.isNotEmpty) ...[
                    const SizedBox(height: 2),
                    Text(
                      item.kgoWeight,
                      style: const TextStyle(fontSize: 11, color: AppColors.textLight),
                    ),
                  ],
                  const SizedBox(height: 4),
                  Text(
                    '${_formatSom(item.kgoPricePerUnit)} ${ref.tr('som')}',
                    style: const TextStyle(
                      fontSize: 14, fontWeight: FontWeight.w700, color: AppColors.terracotta,
                    ),
                  ),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(
                color: AppColors.saffron,
                borderRadius: BorderRadius.circular(AppRadius.pill),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.add_shopping_cart, size: 14, color: Colors.white),
                  const SizedBox(width: 4),
                  Text(
                    ref.tr('karzinka_add'),
                    style: const TextStyle(
                      color: Colors.white, fontSize: 11, fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _openProduct(BuildContext context, WidgetRef ref) async {
    if (item.kgoProductUrl.isEmpty) return;
    final uri = Uri.parse(item.kgoProductUrl);
    final ok = await launchUrl(uri, mode: LaunchMode.externalApplication);
    if (!ok && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(ref.tr('karzinka_open_failed'))),
      );
    }
  }

  String _formatSom(String? amountStr) {
    final v = double.tryParse(amountStr ?? '') ?? 0;
    return NumberFormat('#,###', 'ru').format(v);
  }
}

