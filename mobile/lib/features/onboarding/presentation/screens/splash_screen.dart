import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/router/app_routes.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/widgets/section_card.dart';
import '../../../auth/presentation/providers/auth_state.dart';

/// 3a — Splash Screen.
/// Auth yuklanguncha ko'rsatiladi. Router redirect avtomatik yo'naltiradi.
/// Fallback: 4 sekunddan keyin agar hali splash'da bo'lsa — login'ga.
class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen> {
  Timer? _fallbackTimer;

  @override
  void initState() {
    super.initState();
    // Fallback: 4 sekunddan keyin agar hali splash'da bo'lsa — login'ga
    _fallbackTimer = Timer(const Duration(seconds: 4), () {
      if (!mounted) return;
      final auth = ref.read(authProvider);
      if (auth.isLoading || auth.hasError || !auth.hasValue) {
        context.go(AppRoutes.login);
      }
    });
  }

  @override
  void dispose() {
    _fallbackTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Auth'ni watch qilamiz — router avtomatik redirect qiladi
    ref.watch(authProvider);

    return Scaffold(
      backgroundColor: AppColors.terracotta,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 96,
              height: 96,
              decoration: BoxDecoration(
                color: AppColors.creamBg.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(28),
              ),
              alignment: Alignment.center,
              child: const Text('🍽️', style: TextStyle(fontSize: 48)),
            ),
            const SizedBox(height: 28),
            const DisplayTitle('Menu Mate', color: Colors.white, size: 44),
            const SizedBox(height: 12),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40),
              child: Text(
                "Oilangiz uchun har kunlik menyu",
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white.withValues(alpha: 0.9),
                  fontSize: 15,
                  height: 1.4,
                ),
              ),
            ),
            const SizedBox(height: 40),
            SizedBox(
              width: 24,
              height: 24,
              child: CircularProgressIndicator(
                strokeWidth: 2.5,
                valueColor: AlwaysStoppedAnimation(Colors.white.withValues(alpha: 0.7)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
