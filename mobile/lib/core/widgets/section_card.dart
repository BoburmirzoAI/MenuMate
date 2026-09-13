import 'package:flutter/material.dart';

import '../theme/app_spacing.dart';

/// Ochroq (krem) fonli karta — Dashboard va Menyu ekranlarida ishlatiladi.
class SectionCard extends StatelessWidget {
  const SectionCard({
    super.key,
    required this.child,
    this.color,
    this.padding = const EdgeInsets.all(AppSpacing.xl),
    this.borderRadius,
    this.onTap,
  });

  final Widget child;
  final Color? color;
  final EdgeInsets padding;
  final double? borderRadius;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final radius = BorderRadius.circular(borderRadius ?? AppRadius.xxl);
    final decoration = BoxDecoration(
      color: color ?? Colors.white,
      borderRadius: radius,
    );

    final content = Padding(padding: padding, child: child);

    if (onTap == null) {
      return DecoratedBox(decoration: decoration, child: content);
    }
    return Material(
      color: color ?? Colors.white,
      borderRadius: radius,
      child: InkWell(
        onTap: onTap,
        borderRadius: radius,
        child: content,
      ),
    );
  }
}

/// Fraunces shrift bilan katta sarlavha.
class DisplayTitle extends StatelessWidget {
  const DisplayTitle(
    this.text, {
    super.key,
    this.color,
    this.size = 32,
    this.weight = FontWeight.w600,
    this.align,
  });

  final String text;
  final Color? color;
  final double size;
  final FontWeight weight;
  final TextAlign? align;

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      textAlign: align,
      style: TextStyle(
        fontFamily: 'Fraunces',
        fontSize: size,
        fontWeight: weight,
        height: 1.1,
        letterSpacing: -0.02 * size,
        color: color ?? Theme.of(context).colorScheme.onSurface,
      ),
    );
  }
}
