import 'package:flutter/material.dart';

import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';

/// Ovqat yoki ingredient rasmi.
/// URL bo'lsa — real rasm; aks holda emoji fallback.
class FoodImage extends StatelessWidget {
  const FoodImage({
    super.key,
    required this.imageUrl,
    required this.emoji,
    this.size = 56,
    this.radius,
    this.background,
    this.emojiSize,
  });

  final String imageUrl;
  final String emoji;
  final double size;
  final double? radius;
  final Color? background;
  final double? emojiSize;

  @override
  Widget build(BuildContext context) {
    final r = radius ?? AppRadius.md;
    final bg = background ?? AppColors.creamCard;

    if (imageUrl.isEmpty) {
      return Container(
        width: size, height: size,
        decoration: BoxDecoration(
          color: bg,
          borderRadius: BorderRadius.circular(r),
        ),
        alignment: Alignment.center,
        child: Text(emoji, style: TextStyle(fontSize: emojiSize ?? size * 0.5)),
      );
    }

    return ClipRRect(
      borderRadius: BorderRadius.circular(r),
      child: Image.network(
        imageUrl,
        width: size, height: size, fit: BoxFit.cover,
        errorBuilder: (_, _, _) => Container(
          width: size, height: size,
          color: bg,
          alignment: Alignment.center,
          child: Text(emoji, style: TextStyle(fontSize: emojiSize ?? size * 0.5)),
        ),
        loadingBuilder: (_, child, prog) {
          if (prog == null) return child;
          return Container(
            width: size, height: size,
            color: bg,
            alignment: Alignment.center,
            child: SizedBox(
              width: size * 0.25, height: size * 0.25,
              child: CircularProgressIndicator(
                strokeWidth: 2, color: AppColors.terracotta.withValues(alpha: 0.5),
              ),
            ),
          );
        },
      ),
    );
  }
}
