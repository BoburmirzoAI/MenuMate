import 'package:flutter/material.dart';

import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';
import 'primary_button.dart';

/// Chiroyli dialog — brand ranglar, katta padding, aniq tugmalar.
///
/// Foydalanish:
/// ```dart
/// final result = await AppDialog.show<String>(
///   context: context,
///   title: 'Oila nomi',
///   builder: (ctx) => TextField(...),
///   confirmLabel: 'Saqlash',
///   onConfirm: () => Navigator.of(ctx).pop(controller.text),
/// );
/// ```
class AppDialog extends StatelessWidget {
  const AppDialog({
    super.key,
    required this.title,
    required this.child,
    this.subtitle,
    this.icon,
    this.iconColor,
    this.confirmLabel,
    this.onConfirm,
    this.cancelLabel = 'Bekor',
    this.destructive = false,
    this.confirmLoading = false,
  });

  final String title;
  final String? subtitle;
  final IconData? icon;
  final Color? iconColor;
  final Widget child;
  final String? confirmLabel;
  final VoidCallback? onConfirm;
  final String cancelLabel;
  final bool destructive;
  final bool confirmLoading;

  static Future<T?> show<T>({
    required BuildContext context,
    required Widget dialog,
  }) {
    return showDialog<T>(
      context: context,
      barrierColor: Colors.black.withValues(alpha: 0.4),
      builder: (_) => dialog,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.symmetric(horizontal: AppSpacing.xxl),
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.xxl),
        decoration: BoxDecoration(
          color: AppColors.creamBg,
          borderRadius: BorderRadius.circular(AppRadius.xxl),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                if (icon != null) ...[
                  Container(
                    width: 40, height: 40,
                    decoration: BoxDecoration(
                      color: (iconColor ?? AppColors.terracotta).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(AppRadius.md),
                    ),
                    alignment: Alignment.center,
                    child: Icon(icon, color: iconColor ?? AppColors.terracotta, size: 22),
                  ),
                  const SizedBox(width: AppSpacing.md),
                ],
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: const TextStyle(
                          fontFamily: 'Fraunces',
                          fontSize: 20,
                          fontWeight: FontWeight.w700,
                          color: AppColors.textDark,
                        ),
                      ),
                      if (subtitle != null) ...[
                        const SizedBox(height: 2),
                        Text(
                          subtitle!,
                          style: TextStyle(
                            fontSize: 13, color: AppColors.textMedium,
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
                GestureDetector(
                  onTap: () => Navigator.of(context).pop(),
                  child: Container(
                    width: 32, height: 32,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.close, size: 18, color: AppColors.textMedium),
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.xl),
            child,
            if (confirmLabel != null) ...[
              const SizedBox(height: AppSpacing.xl),
              Row(
                children: [
                  Expanded(
                    child: SecondaryButton(
                      label: cancelLabel,
                      onPressed: () => Navigator.of(context).pop(),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: PrimaryButton(
                      label: confirmLabel!,
                      onPressed: confirmLoading ? null : onConfirm,
                      isLoading: confirmLoading,
                      color: destructive ? AppColors.error : null,
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }
}
