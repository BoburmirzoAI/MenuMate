import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/router/app_routes.dart';
import '../../../../core/storage/preferences.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/primary_button.dart';
import '../../../../core/widgets/section_card.dart';

/// 3c — Onboarding (3 sahifa slider).
class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  final _controller = PageController();
  int _page = 0;

  final _pages = const [
    (
      emoji: '👨‍👩‍👧',
      color: AppColors.creamCard,
      title: 'Oilaga mos menyu',
      subtitle: "Har kuni ovqat haqida o'ylab qolmang — biz sizga tayyor rejani beramiz",
    ),
    (
      emoji: '💚',
      color: AppColors.creamAccent,
      title: 'Salomatlik hisobga olinadi',
      subtitle: 'Allergiya, diabet, sog\'liq holati — hammasi bilan menyu tuziladi',
    ),
    (
      emoji: '🛒',
      color: AppColors.creamCard,
      title: 'Xarid ro\'yxati tayyor',
      subtitle: 'Bozorga borishda nima olishni bilib, vaqt tejaysiz',
    ),
  ];

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _finish() async {
    await ref.read(preferencesProvider).setOnboardingSeen(true);
    if (mounted) context.go(AppRoutes.languageSelect);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            // Skip tugma
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: AppSpacing.sm),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: _finish,
                    child: const Text("O'tkazish"),
                  ),
                ],
              ),
            ),
            // Slides
            Expanded(
              child: PageView.builder(
                controller: _controller,
                itemCount: _pages.length,
                onPageChanged: (i) => setState(() => _page = i),
                itemBuilder: (context, i) {
                  final p = _pages[i];
                  return Padding(
                    padding: const EdgeInsets.all(AppSpacing.xxl),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          width: 220,
                          height: 220,
                          decoration: BoxDecoration(
                            color: p.color,
                            borderRadius: BorderRadius.circular(AppRadius.xxl + 12),
                          ),
                          alignment: Alignment.center,
                          child: Text(p.emoji, style: const TextStyle(fontSize: 96)),
                        ),
                        const SizedBox(height: AppSpacing.huge),
                        DisplayTitle(p.title, size: 32, align: TextAlign.center),
                        const SizedBox(height: AppSpacing.lg),
                        Text(
                          p.subtitle,
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            color: AppColors.textMedium,
                            fontSize: 16,
                            height: 1.5,
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            // Dots
            Padding(
              padding: const EdgeInsets.symmetric(vertical: AppSpacing.xl),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(_pages.length, (i) {
                  final active = i == _page;
                  return AnimatedContainer(
                    duration: const Duration(milliseconds: 250),
                    margin: const EdgeInsets.symmetric(horizontal: 4),
                    width: active ? 24 : 8,
                    height: 8,
                    decoration: BoxDecoration(
                      color: active ? AppColors.terracotta : AppColors.textLight.withValues(alpha: 0.3),
                      borderRadius: BorderRadius.circular(4),
                    ),
                  );
                }),
              ),
            ),
            // CTA
            Padding(
              padding: const EdgeInsets.fromLTRB(AppSpacing.xxl, 0, AppSpacing.xxl, AppSpacing.xxl),
              child: PrimaryButton(
                label: _page == _pages.length - 1 ? 'Boshlash' : 'Keyingi',
                onPressed: () {
                  if (_page == _pages.length - 1) {
                    _finish();
                  } else {
                    _controller.nextPage(
                      duration: const Duration(milliseconds: 300),
                      curve: Curves.easeInOut,
                    );
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
