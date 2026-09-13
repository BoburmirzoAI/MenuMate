import 'package:flutter/material.dart';

import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';
import 'section_card.dart';

/// Brand-uslubdagi bottom sheet — grabber, chiroyli header, katta padding.
///
/// Foydalanish:
/// ```dart
/// final result = await AppBottomSheet.show<String>(
///   context: context,
///   title: 'Shahar tanlash',
///   child: Wrap(...),
/// );
/// ```
class AppBottomSheet extends StatelessWidget {
  const AppBottomSheet({
    super.key,
    required this.title,
    required this.child,
    this.subtitle,
    this.scrollable = false,
  });

  final String title;
  final String? subtitle;
  final Widget child;
  final bool scrollable;

  static Future<T?> show<T>({
    required BuildContext context,
    required String title,
    required Widget child,
    String? subtitle,
    bool scrollable = false,
    bool isDismissible = true,
  }) {
    return showModalBottomSheet<T>(
      context: context,
      isScrollControlled: scrollable,
      isDismissible: isDismissible,
      backgroundColor: Colors.transparent,
      builder: (_) => AppBottomSheet(
        title: title,
        subtitle: subtitle,
        scrollable: scrollable,
        child: child,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final content = Container(
      decoration: const BoxDecoration(
        color: AppColors.creamBg,
        borderRadius: BorderRadius.vertical(top: Radius.circular(AppRadius.xxl)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Grabber
          Container(
            margin: const EdgeInsets.only(top: 10, bottom: 6),
            width: 40, height: 4,
            decoration: BoxDecoration(
              color: AppColors.textLight.withValues(alpha: 0.3),
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(
              AppSpacing.xxl, AppSpacing.md, AppSpacing.lg, AppSpacing.md,
            ),
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      DisplayTitle(title, size: 22),
                      if (subtitle != null) ...[
                        const SizedBox(height: 2),
                        Text(
                          subtitle!,
                          style: TextStyle(fontSize: 13, color: AppColors.textMedium),
                        ),
                      ],
                    ],
                  ),
                ),
                GestureDetector(
                  onTap: () => Navigator.of(context).pop(),
                  child: Container(
                    width: 34, height: 34,
                    decoration: const BoxDecoration(
                      color: Colors.white, shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.close, size: 18, color: AppColors.textMedium),
                  ),
                ),
              ],
            ),
          ),
          Flexible(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(
                AppSpacing.xxl, 0, AppSpacing.xxl, AppSpacing.xxl,
              ),
              child: child,
            ),
          ),
          SizedBox(height: MediaQuery.paddingOf(context).bottom),
        ],
      ),
    );

    if (scrollable) {
      // Ekran balandligining 85%igacha cho'ziladi
      return ConstrainedBox(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.sizeOf(context).height * 0.85,
        ),
        child: content,
      );
    }
    return content;
  }
}
