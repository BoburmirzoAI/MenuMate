import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'app_colors.dart';
import 'app_spacing.dart';

/// Material 3 tema — Claude Design HTML asosida.
class AppTheme {
  AppTheme._();

  static ThemeData get light => _buildTheme(Brightness.light);
  static ThemeData get dark => _buildTheme(Brightness.dark);

  static TextStyle heading(double size, {FontWeight weight = FontWeight.w600, Color? color}) =>
      GoogleFonts.fraunces(
        fontSize: size,
        fontWeight: weight,
        letterSpacing: -0.02 * size,
        height: 1.1,
        color: color,
      );

  static TextStyle body(double size, {FontWeight weight = FontWeight.w400, Color? color}) =>
      GoogleFonts.inter(
        fontSize: size,
        fontWeight: weight,
        height: 1.4,
        color: color,
      );

  static ThemeData _buildTheme(Brightness brightness) {
    final isLight = brightness == Brightness.light;

    final colorScheme = ColorScheme.fromSeed(
      seedColor: AppColors.terracotta,
      brightness: brightness,
      primary: AppColors.terracotta,
      secondary: AppColors.saffron,
      surface: isLight ? AppColors.creamBg : AppColors.darkBg,
      onSurface: isLight ? AppColors.textDark : Colors.white,
      error: AppColors.error,
    );

    final baseTextTheme = isLight ? ThemeData.light().textTheme : ThemeData.dark().textTheme;
    final textColor = isLight ? AppColors.textDark : Colors.white;

    final textTheme = baseTextTheme.copyWith(
      displayLarge: GoogleFonts.fraunces(fontSize: 52, fontWeight: FontWeight.w600, letterSpacing: -1, color: textColor),
      displayMedium: GoogleFonts.fraunces(fontSize: 40, fontWeight: FontWeight.w600, letterSpacing: -0.8, color: textColor),
      displaySmall: GoogleFonts.fraunces(fontSize: 32, fontWeight: FontWeight.w600, letterSpacing: -0.5, color: textColor),
      headlineLarge: GoogleFonts.fraunces(fontSize: 28, fontWeight: FontWeight.w600, letterSpacing: -0.5, color: textColor),
      headlineMedium: GoogleFonts.fraunces(fontSize: 24, fontWeight: FontWeight.w600, color: textColor),
      headlineSmall: GoogleFonts.fraunces(fontSize: 20, fontWeight: FontWeight.w600, color: textColor),
      titleLarge: GoogleFonts.inter(fontSize: 18, fontWeight: FontWeight.w600, color: textColor),
      titleMedium: GoogleFonts.inter(fontSize: 16, fontWeight: FontWeight.w600, color: textColor),
      titleSmall: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w600, color: textColor),
      bodyLarge: GoogleFonts.inter(fontSize: 16, color: textColor),
      bodyMedium: GoogleFonts.inter(fontSize: 14, color: textColor),
      bodySmall: GoogleFonts.inter(fontSize: 13, color: AppColors.textMedium),
      labelLarge: GoogleFonts.inter(fontSize: 15, fontWeight: FontWeight.w600, color: textColor),
      labelMedium: GoogleFonts.inter(fontSize: 13, fontWeight: FontWeight.w500, color: textColor),
      labelSmall: GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w500, color: AppColors.textLight),
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: textTheme,
      scaffoldBackgroundColor: colorScheme.surface,

      appBarTheme: AppBarTheme(
        backgroundColor: colorScheme.surface,
        foregroundColor: textColor,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.fraunces(
          fontSize: 24,
          fontWeight: FontWeight.w600,
          letterSpacing: -0.5,
          color: textColor,
        ),
        iconTheme: IconThemeData(color: textColor),
      ),

      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.terracotta,
          foregroundColor: Colors.white,
          minimumSize: const Size.fromHeight(56),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.lg)),
          elevation: 0,
          textStyle: GoogleFonts.inter(fontSize: 16, fontWeight: FontWeight.w600),
        ),
      ),

      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          minimumSize: const Size.fromHeight(56),
          foregroundColor: AppColors.textDark,
          side: BorderSide(color: AppColors.textDark.withValues(alpha: 0.2)),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.lg)),
          textStyle: GoogleFonts.inter(fontSize: 16, fontWeight: FontWeight.w500),
        ),
      ),

      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(foregroundColor: AppColors.terracotta),
      ),

      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: isLight ? Colors.white : AppColors.darkCard,
        contentPadding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: 18),
        hintStyle: GoogleFonts.inter(color: AppColors.textLight, fontSize: 15),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.md),
          borderSide: BorderSide(color: AppColors.textLight.withValues(alpha: 0.3)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.md),
          borderSide: BorderSide(color: AppColors.textLight.withValues(alpha: 0.3)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.md),
          borderSide: const BorderSide(color: AppColors.terracotta, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.md),
          borderSide: const BorderSide(color: AppColors.error, width: 1.5),
        ),
      ),

      cardTheme: CardThemeData(
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.xl)),
        color: isLight ? Colors.white : AppColors.darkCard,
        margin: EdgeInsets.zero,
      ),

      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: isLight ? Colors.white : AppColors.darkSurface,
        indicatorColor: AppColors.terracotta.withValues(alpha: 0.15),
        labelTextStyle: WidgetStatePropertyAll(
          GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w500),
        ),
      ),

      chipTheme: ChipThemeData(
        backgroundColor: AppColors.creamCard,
        selectedColor: AppColors.terracotta,
        labelStyle: GoogleFonts.inter(fontSize: 13, fontWeight: FontWeight.w500),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.pill)),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      ),
    );
  }
}
