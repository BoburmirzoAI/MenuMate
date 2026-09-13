import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/api/simple_repositories.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/food_image.dart';
import '../../../../core/widgets/section_card.dart';
import '../../../../core/widgets/state_views.dart';
import '../../../menu/data/menu_repository.dart';
import '../../state/shopping_checks_provider.dart';
import 'karzinka_transfer_screen.dart';

/// Xarid ro'yxati — Karzinka Go integratsiyasi bilan (mock).
class ShoppingScreen extends ConsumerWidget {
  const ShoppingScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final menuAsync = ref.watch(currentMenuProvider);

    return Scaffold(
      body: SafeArea(
        child: menuAsync.when(
          loading: () => const LoadingView(),
          error: (e, _) => ErrorRetryView(
            message: e is ApiException ? e.message : '$e',
            onRetry: () => ref.invalidate(currentMenuProvider),
          ),
          data: (menu) {
            if (menu == null) return const _NoMenuMessage();
            return _ShoppingContent(menuId: menu.id, menuDuration: menu.duration);
          },
        ),
      ),
    );
  }
}

class _ShoppingContent extends ConsumerWidget {
  const _ShoppingContent({required this.menuId, required this.menuDuration});

  final int menuId;
  final String menuDuration;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final listAsync = ref.watch(shoppingListProvider(menuId));

    return listAsync.when(
      loading: () => const LoadingView(),
      error: (err, _) => ErrorRetryView(
        message: err is ApiException ? err.message : ref.tr('error'),
        onRetry: () => ref.invalidate(shoppingListProvider(menuId)),
      ),
      data: (list) {
        if (list.totalItems == 0) return const _EmptyMessage();

        // Tanlangan (isPurchased=true) qatorlarning jami narxini hisoblaymiz.
        final localChecks = ref.watch(shoppingLocalChecksProvider);
        final selectedTotal = _computeSelectedTotal(list, localChecks);
        final selectedCount = _countSelected(list, localChecks);

        return RefreshIndicator(
          onRefresh: () async => ref.invalidate(shoppingListProvider(menuId)),
          child: CustomScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
          slivers: [
            SliverToBoxAdapter(child: _Header(list: list, duration: menuDuration)),
            SliverToBoxAdapter(
              child: _KgoBanner(
                selectedCount: selectedCount,
                totalCount: list.totalItems,
                selectedTotal: selectedTotal,
              ),
            ),
            for (final entry in list.itemsByCategory.entries)
              SliverToBoxAdapter(
                child: _CategoryGroup(
                  category: entry.key,
                  items: entry.value,
                ),
              ),
            if (list.unavailableItems.isNotEmpty)
              SliverToBoxAdapter(child: _UnavailableBlock(items: list.unavailableItems)),
            SliverToBoxAdapter(child: _TransferCta(selectedTotal: selectedTotal)),
            const SliverToBoxAdapter(child: SizedBox(height: 100)),
          ],
          ),
        );
      },
    );
  }
}

// ============================================================================
// Real-time hisob: local checkbox holati + jami narx yordamchilari
// ============================================================================

double _itemPrice(ShoppingItem item) =>
    double.tryParse(item.priceTotal ?? '') ?? 0;

double _computeSelectedTotal(ShoppingList list, Map<int, bool> overrides) {
  double total = 0;
  for (final items in list.itemsByCategory.values) {
    for (final it in items) {
      final checked = overrides[it.id] ?? it.isPurchased;
      if (checked && it.kgoAvailable) total += _itemPrice(it);
    }
  }
  return total;
}

int _countSelected(ShoppingList list, Map<int, bool> overrides) {
  int n = 0;
  for (final items in list.itemsByCategory.values) {
    for (final it in items) {
      if (overrides[it.id] ?? it.isPurchased) n++;
    }
  }
  return n;
}

// ============================================================================
// Header
// ============================================================================

class _Header extends ConsumerWidget {
  const _Header({required this.list, required this.duration});
  final ShoppingList list;
  final String duration;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final periodLabel = duration == 'MONTHLY'
        ? ref.tr('menu_days_30')
        : ref.tr('menu_days_7');
    return Padding(
      padding: const EdgeInsets.fromLTRB(
        AppSpacing.xxl, AppSpacing.lg, AppSpacing.xxl, AppSpacing.md,
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                DisplayTitle(ref.tr('shopping_title'), size: 26),
                const SizedBox(height: 4),
                Text(
                  '$periodLabel · ${list.totalItems} ${ref.tr('shopping_kgo_items_of')}',
                  style: TextStyle(color: AppColors.textMedium, fontSize: 13),
                ),
              ],
            ),
          ),
          IconButton.filled(
            onPressed: () => _copyToClipboard(context, list),
            icon: const Icon(Icons.upload_outlined),
            style: IconButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: AppColors.textDark,
              side: BorderSide(color: AppColors.creamCard),
            ),
          ),
        ],
      ),
    );
  }

  void _copyToClipboard(BuildContext context, ShoppingList list) {
    final buf = StringBuffer("Xarid ro'yxati:\n");
    list.itemsByCategory.forEach((cat, items) {
      buf.writeln('\n${_categoryLabel(cat)}:');
      for (final it in items) {
        buf.writeln('  • ${it.ingredientName} — ${it.totalAmount} ${it.unit}');
      }
    });
    Clipboard.setData(ClipboardData(text: buf.toString()));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('OK')),
    );
  }
}

// ============================================================================
// Karzinka Go banner
// ============================================================================

class _KgoBanner extends ConsumerWidget {
  const _KgoBanner({
    required this.selectedCount,
    required this.totalCount,
    required this.selectedTotal,
  });
  final int selectedCount;
  final int totalCount;
  final double selectedTotal;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final total = _formatDouble(selectedTotal);
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl, vertical: AppSpacing.sm),
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.lg),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF4A2E1F), Color(0xFF3A2417)],
            begin: Alignment.centerLeft,
            end: Alignment.centerRight,
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
                  Row(
                    children: [
                      Text(
                        ref.tr('shopping_kgo_connected'),
                        style: const TextStyle(
                          fontSize: 13, fontWeight: FontWeight.w700, color: Colors.white,
                        ),
                      ),
                      const SizedBox(width: 6),
                      Container(
                        width: 6, height: 6,
                        decoration: const BoxDecoration(
                          color: AppColors.success,
                          shape: BoxShape.circle,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  RichText(
                    text: TextSpan(
                      children: [
                        TextSpan(
                          text: '${ref.tr('shopping_kgo_selected')} ',
                          style: TextStyle(
                            fontSize: 12, color: Colors.white.withValues(alpha: 0.7),
                          ),
                        ),
                        TextSpan(
                          text: '$total ${ref.tr('som')}',
                          style: const TextStyle(
                            fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.saffron,
                          ),
                        ),
                        TextSpan(
                          text: ' · $selectedCount/$totalCount',
                          style: TextStyle(
                            fontSize: 12, color: Colors.white.withValues(alpha: 0.7),
                          ),
                        ),
                      ],
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
}

// ============================================================================
// Kategoriya guruhi
// ============================================================================

class _CategoryGroup extends ConsumerStatefulWidget {
  const _CategoryGroup({required this.category, required this.items});
  final String category;
  final List<ShoppingItem> items;

  @override
  ConsumerState<_CategoryGroup> createState() => _CategoryGroupState();
}

class _CategoryGroupState extends ConsumerState<_CategoryGroup> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    final overrides = ref.watch(shoppingLocalChecksProvider);
    final purchased = widget.items
        .where((it) => overrides[it.id] ?? it.isPurchased)
        .length;
    final total = widget.items.length;
    final color = _categoryColor(widget.category);

    return Padding(
      padding: const EdgeInsets.fromLTRB(
        AppSpacing.xxl, AppSpacing.sm, AppSpacing.xxl, AppSpacing.sm,
      ),
      child: SectionCard(
        color: Colors.white,
        padding: EdgeInsets.zero,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header — bosilganda ochilib/yopiladi
            InkWell(
              onTap: () => setState(() => _expanded = !_expanded),
              borderRadius: BorderRadius.circular(AppRadius.lg),
              child: Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: _expanded ? AppColors.creamCard : Colors.white,
                  borderRadius: BorderRadius.only(
                    topLeft: const Radius.circular(AppRadius.lg),
                    topRight: const Radius.circular(AppRadius.lg),
                    bottomLeft: Radius.circular(_expanded ? 0 : AppRadius.lg),
                    bottomRight: Radius.circular(_expanded ? 0 : AppRadius.lg),
                  ),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 42, height: 42,
                      decoration: BoxDecoration(
                        color: color,
                        borderRadius: BorderRadius.circular(AppRadius.sm),
                      ),
                      alignment: Alignment.center,
                      child: Text(
                        _categoryEmoji(widget.category),
                        style: const TextStyle(fontSize: 20),
                      ),
                    ),
                    const SizedBox(width: AppSpacing.md),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            _categoryLabel(widget.category),
                            style: const TextStyle(
                              fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.textDark,
                            ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            '$total ${ref.tr('shopping_kgo_items_of')} · $purchased ✓',
                            style: const TextStyle(fontSize: 12, color: AppColors.textLight),
                          ),
                        ],
                      ),
                    ),
                    if (!_expanded && purchased > 0) ...[
                      _MiniProgress(purchased: purchased, total: total),
                      const SizedBox(width: 6),
                    ],
                    Icon(
                      _expanded ? Icons.expand_less : Icons.chevron_right,
                      color: AppColors.textLight,
                    ),
                  ],
                ),
              ),
            ),
            if (_expanded)
              Column(
                children: [
                  for (int i = 0; i < widget.items.length; i++) ...[
                    _ItemRow(item: widget.items[i]),
                    if (i != widget.items.length - 1)
                      const Divider(height: 1, indent: 60),
                  ],
                ],
              ),
          ],
        ),
      ),
    );
  }
}

/// Yopiq kategoriya ichida — kichik yashil taraqqiy chizig'i.
class _MiniProgress extends StatelessWidget {
  const _MiniProgress({required this.purchased, required this.total});
  final int purchased;
  final int total;

  @override
  Widget build(BuildContext context) {
    final ratio = total == 0 ? 0.0 : purchased / total;
    return SizedBox(
      width: 44, height: 6,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(3),
        child: Stack(
          children: [
            Container(color: AppColors.creamCard),
            FractionallySizedBox(
              widthFactor: ratio.clamp(0.0, 1.0),
              child: Container(color: AppColors.success),
            ),
          ],
        ),
      ),
    );
  }
}

/// Kategoriya uchun mockup'dagi ranglar.
Color _categoryColor(String cat) {
  switch (cat) {
    case 'MEAT': return const Color(0xFFB84C3A);       // to'q qizil
    case 'VEGETABLE': return const Color(0xFF7BA05B);   // yashil
    case 'FRUIT': return const Color(0xFFE07B4B);       // to'q sariq
    case 'DAIRY': return const Color(0xFF89A9C4);       // ko'k
    case 'GRAIN': return const Color(0xFFE0A93A);       // saffron
    case 'SPICE': return const Color(0xFFCF6B32);       // ziravor
    case 'OIL': return const Color(0xFF8B9A45);         // zaytun
    default: return AppColors.textLight;
  }
}

class _ItemRow extends ConsumerWidget {
  const _ItemRow({required this.item});
  final ShoppingItem item;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final checked = ref.watch(shoppingLocalChecksProvider)[item.id] ?? item.isPurchased;
    final decoration = checked ? TextDecoration.lineThrough : TextDecoration.none;
    final nameColor = checked ? AppColors.textLight : AppColors.textDark;
    final amountColor = checked ? AppColors.textLight : AppColors.textDark;

    final priceLabel = _formatSom(item.priceTotal);

    return InkWell(
      onTap: item.kgoAvailable ? () => _toggle(ref, !checked) : null,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 12),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Checkbox(
              value: checked,
              onChanged: item.kgoAvailable ? (v) => _toggle(ref, v ?? false) : null,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
            ),
            FoodImage(
              imageUrl: item.ingredientImageUrl,
              emoji: _categoryEmoji(item.ingredientCategory),
              size: 40,
              radius: AppRadius.sm,
              background: AppColors.creamBg,
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    item.ingredientName,
                    style: TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w700,
                      color: nameColor,
                      decoration: decoration,
                    ),
                  ),
                  if (item.kgoAvailable && item.priceTotal != null) ...[
                    const SizedBox(height: 2),
                    Text(
                      '$priceLabel so\'m',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: checked ? AppColors.textLight : AppColors.terracotta,
                        decoration: decoration,
                      ),
                    ),
                  ],
                ],
              ),
            ),
            if (!item.kgoAvailable)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.error,
                  borderRadius: BorderRadius.circular(AppRadius.sm),
                ),
                child: Text(
                  ref.tr('shopping_kgo_unavailable_badge'),
                  style: const TextStyle(
                    fontSize: 9, fontWeight: FontWeight.w700, color: Colors.white,
                  ),
                ),
              )
            else
              Text(
                '${item.totalAmount} ${item.unit}',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: amountColor,
                  decoration: decoration,
                ),
              ),
          ],
        ),
      ),
    );
  }

  void _toggle(WidgetRef ref, bool value) async {
    // Darhol local UIga aks etamiz (real-time)
    ref.read(shoppingLocalChecksProvider.notifier).toggle(item.id, value);
    // Keyin backend'ga saqlaymiz (fon rejimida, natijasini kutmasdan)
    try {
      await ref.read(productsRepositoryProvider).toggleItem(item.id, value);
    } on ApiException {
      // xatoni jimgina o'tkazamiz
    }
  }
}

// ============================================================================
// Qolmagan mahsulotlar bloki
// ============================================================================

class _UnavailableBlock extends ConsumerWidget {
  const _UnavailableBlock({required this.items});
  final List<ShoppingItem> items;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Padding(
      padding: const EdgeInsets.all(AppSpacing.xxl),
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.lg),
        decoration: BoxDecoration(
          color: AppColors.warning.withValues(alpha: 0.12),
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.warning_amber_rounded, size: 18, color: AppColors.warning),
                const SizedBox(width: 6),
                Expanded(
                  child: Text(
                    ref.tr('shopping_kgo_unavailable_title'),
                    style: const TextStyle(
                      fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textDark,
                    ),
                  ),
                ),
                GestureDetector(
                  onTap: () => _copy(context),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.textDark,
                      borderRadius: BorderRadius.circular(AppRadius.pill),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.copy, size: 12, color: Colors.white),
                        const SizedBox(width: 4),
                        Text(ref.tr('copy'),
                            style: const TextStyle(fontSize: 11, color: Colors.white)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              '${items.length} ${ref.tr('shopping_kgo_unavailable_sub')}',
              style: TextStyle(fontSize: 11, color: AppColors.textMedium),
            ),
            const SizedBox(height: 8),
            for (final it in items)
              Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text(
                  '• ${it.ingredientName} — ${it.totalAmount} ${it.unit}',
                  style: const TextStyle(fontSize: 13, color: AppColors.textDark),
                ),
              ),
          ],
        ),
      ),
    );
  }

  void _copy(BuildContext context) {
    final text = items
        .map((i) => '${i.ingredientName} — ${i.totalAmount} ${i.unit}')
        .join('\n');
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Nusxa olindi')),
    );
  }
}

// ============================================================================
// Katta CTA — Karzinka Go ga o'tkazish
// ============================================================================

class _TransferCta extends ConsumerWidget {
  const _TransferCta({required this.selectedTotal});
  final double selectedTotal;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final total = _formatDouble(selectedTotal);
    final disabled = selectedTotal <= 0;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl, vertical: AppSpacing.md),
      child: ElevatedButton(
        onPressed: disabled
            ? null
            : () => Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => const KarzinkaTransferScreen(),
                  ),
                ),
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.saffron,
          foregroundColor: Colors.white,
          disabledBackgroundColor: AppColors.creamAccent,
          disabledForegroundColor: AppColors.textLight,
          minimumSize: const Size.fromHeight(56),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.lg)),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.shopping_cart, size: 20),
                const SizedBox(width: 8),
                Text(
                  ref.tr('shopping_transfer_cta'),
                  style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 15),
                ),
              ],
            ),
            const SizedBox(height: 2),
            Text(
              disabled
                  ? ref.tr('shopping_no_selection')
                  : '$total ${ref.tr('som')}',
              style: const TextStyle(
                fontSize: 13, fontWeight: FontWeight.w700, color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================================
// Placeholder ekranlar
// ============================================================================

class _NoMenuMessage extends ConsumerWidget {
  const _NoMenuMessage();
  @override
  Widget build(BuildContext context, WidgetRef ref) => Center(
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.xxxl),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('🛒', style: TextStyle(fontSize: 56)),
              const SizedBox(height: AppSpacing.md),
              DisplayTitle(ref.tr('shopping_no_menu_title'), size: 20),
              const SizedBox(height: 6),
              Text(
                ref.tr('shopping_no_menu_body'),
                textAlign: TextAlign.center,
                style: TextStyle(color: AppColors.textMedium),
              ),
            ],
          ),
        ),
      );
}

class _EmptyMessage extends ConsumerWidget {
  const _EmptyMessage();
  @override
  Widget build(BuildContext context, WidgetRef ref) => Center(
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.xxxl),
          child: Text(
            ref.tr('shopping_empty_body'),
            textAlign: TextAlign.center,
            style: TextStyle(color: AppColors.textMedium),
          ),
        ),
      );
}

// ============================================================================
// Yordamchilar
// ============================================================================

String _formatSom(String? amountStr) {
  if (amountStr == null || amountStr.isEmpty) return '0';
  return _formatDouble(double.tryParse(amountStr) ?? 0);
}

/// So'm formati — minglar bo'sh joy bilan, kasr qismi bo'lsa 2 raqamgacha
/// (masalan: `4 100,68`; nol kasr bo'lsa — `4 100`).
String _formatDouble(double v) {
  final hasFraction = (v - v.truncateToDouble()).abs() >= 0.005;
  final pattern = hasFraction ? '#,##0.00' : '#,###';
  return NumberFormat(pattern, 'ru').format(v).replaceAll(' ', ' ');
}

String _categoryLabel(String cat) {
  switch (cat) {
    case 'VEGETABLE': return 'Sabzavotlar';
    case 'FRUIT': return 'Mevalar';
    case 'MEAT': return "Go'sht";
    case 'DAIRY': return 'Sut mahsulotlari';
    case 'GRAIN': return 'Don mahsulotlari';
    case 'SPICE': return 'Ziravorlar';
    case 'OIL': return 'Moylar';
    default: return 'Boshqa';
  }
}

String _categoryEmoji(String cat) {
  switch (cat) {
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

