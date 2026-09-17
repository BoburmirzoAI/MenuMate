import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../l10n/language_provider.dart';
import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';
import 'primary_button.dart';
import 'section_card.dart';

/// Yuklanish holati — markazlashtirilgan terracotta spinner.
class LoadingView extends StatelessWidget {
  const LoadingView({super.key, this.label});
  final String? label;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(
            width: 32, height: 32,
            child: CircularProgressIndicator(strokeWidth: 3, color: AppColors.terracotta),
          ),
          if (label != null) ...[
            const SizedBox(height: AppSpacing.md),
            Text(
              label!,
              style: const TextStyle(color: AppColors.textMedium, fontSize: 13),
            ),
          ],
        ],
      ),
    );
  }
}

/// Bo'sh ro'yxat holati — katta emoji + sarlavha + izoh + ixtiyoriy CTA.
class EmptyView extends StatelessWidget {
  const EmptyView({
    super.key,
    required this.emoji,
    required this.title,
    this.subtitle,
    this.ctaLabel,
    this.onCta,
  });

  final String emoji;
  final String title;
  final String? subtitle;
  final String? ctaLabel;
  final VoidCallback? onCta;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.xxxl),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(emoji, style: const TextStyle(fontSize: 60)),
            const SizedBox(height: AppSpacing.md),
            DisplayTitle(title, size: 20),
            if (subtitle != null) ...[
              const SizedBox(height: 6),
              Text(
                subtitle!,
                textAlign: TextAlign.center,
                style: TextStyle(color: AppColors.textMedium, fontSize: 13),
              ),
            ],
            if (ctaLabel != null && onCta != null) ...[
              const SizedBox(height: AppSpacing.xl),
              PrimaryButton(label: ctaLabel!, onPressed: onCta, fullWidth: false),
            ],
          ],
        ),
      ),
    );
  }
}

/// Xato holati — ikonka + xato matni + "Qayta urinish" tugma.
class ErrorRetryView extends ConsumerWidget {
  const ErrorRetryView({
    super.key,
    required this.message,
    required this.onRetry,
  });

  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.xxxl),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 64, height: 64,
              decoration: BoxDecoration(
                color: AppColors.error.withValues(alpha: 0.12),
                shape: BoxShape.circle,
              ),
              alignment: Alignment.center,
              child: const Icon(Icons.error_outline, color: AppColors.error, size: 32),
            ),
            const SizedBox(height: AppSpacing.md),
            DisplayTitle(ref.tr('error'), size: 18),
            const SizedBox(height: 6),
            Text(
              message,
              textAlign: TextAlign.center,
              style: TextStyle(color: AppColors.textMedium, fontSize: 13),
              maxLines: 4,
              overflow: TextOverflow.ellipsis,
            ),
            const SizedBox(height: AppSpacing.xl),
            PrimaryButton(label: ref.tr('retry'), onPressed: onRetry, fullWidth: false),
          ],
        ),
      ),
    );
  }
}

/// Ro'yxatga qulay skeleton element — shimmer animatsiyasi bilan xira karta.
class ListSkeleton extends StatefulWidget {
  const ListSkeleton({super.key, this.itemHeight = 80, this.itemCount = 5});
  final double itemHeight;
  final int itemCount;

  @override
  State<ListSkeleton> createState() => _ListSkeletonState();
}

class _ListSkeletonState extends State<ListSkeleton>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1400),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(AppSpacing.xxl),
      itemCount: widget.itemCount,
      separatorBuilder: (_, _) => const SizedBox(height: AppSpacing.md),
      itemBuilder: (_, _) => AnimatedBuilder(
        animation: _controller,
        builder: (context, _) {
          final t = _controller.value;
          return Container(
            height: widget.itemHeight,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(AppRadius.lg),
              gradient: LinearGradient(
                begin: Alignment(-1 + 2 * t, 0),
                end: Alignment(1 + 2 * t, 0),
                colors: [
                  AppColors.creamCard.withValues(alpha: 0.4),
                  AppColors.creamCard.withValues(alpha: 0.75),
                  AppColors.creamCard.withValues(alpha: 0.4),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
