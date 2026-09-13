import 'package:flutter/material.dart';

import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';

/// Asosiy CTA tugma — terracotta rangda.
class PrimaryButton extends StatelessWidget {
  const PrimaryButton({
    super.key,
    required this.label,
    this.onPressed,
    this.icon,
    this.isLoading = false,
    this.fullWidth = true,
    this.color,
  });

  final String label;
  final VoidCallback? onPressed;
  final IconData? icon;
  final bool isLoading;
  final bool fullWidth;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    final bg = color ?? AppColors.terracotta;
    final button = ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: bg,
        foregroundColor: Colors.white,
        disabledBackgroundColor: bg.withValues(alpha: 0.5),
        disabledForegroundColor: Colors.white,
        minimumSize: fullWidth ? const Size.fromHeight(56) : const Size(120, 48),
        padding: EdgeInsets.symmetric(
          horizontal: fullWidth ? AppSpacing.xxl : AppSpacing.xl,
        ),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.lg)),
        elevation: 0,
      ),
      child: isLoading
          ? const SizedBox(
              width: 22,
              height: 22,
              child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white),
            )
          : Row(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                if (icon != null) ...[
                  Icon(icon, size: 20),
                  const SizedBox(width: AppSpacing.sm),
                ],
                Text(label),
              ],
            ),
    );
    return button;
  }
}

/// Ikkinchi darajali tugma.
class SecondaryButton extends StatelessWidget {
  const SecondaryButton({
    super.key,
    required this.label,
    this.onPressed,
    this.icon,
    this.fullWidth = true,
  });

  final String label;
  final VoidCallback? onPressed;
  final IconData? icon;
  final bool fullWidth;

  @override
  Widget build(BuildContext context) {
    return OutlinedButton(
      onPressed: onPressed,
      style: OutlinedButton.styleFrom(
        minimumSize: fullWidth ? const Size.fromHeight(56) : const Size(120, 48),
        side: BorderSide(color: AppColors.textDark.withValues(alpha: 0.2)),
        foregroundColor: AppColors.textDark,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.lg)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (icon != null) ...[
            Icon(icon, size: 20),
            const SizedBox(width: AppSpacing.sm),
          ],
          Text(label),
        ],
      ),
    );
  }
}
