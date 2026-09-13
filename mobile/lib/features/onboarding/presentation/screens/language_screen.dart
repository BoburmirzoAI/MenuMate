import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/l10n/language_provider.dart';
import '../../../../core/router/app_routes.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/primary_button.dart';
import '../../../../core/widgets/section_card.dart';

/// 3b — Til tanlash.
class LanguageScreen extends ConsumerStatefulWidget {
  const LanguageScreen({super.key});

  @override
  ConsumerState<LanguageScreen> createState() => _LanguageScreenState();
}

class _LanguageScreenState extends ConsumerState<LanguageScreen> {
  late String _selected;

  @override
  void initState() {
    super.initState();
    _selected = ref.read(languageProvider);
  }

  final _options = const [
    (code: 'uz', flag: '🇺🇿', name: "O'zbek", nativeName: 'Uzbek'),
    (code: 'ru', flag: '🇷🇺', name: 'Русский', nativeName: 'Russian'),
    (code: 'en', flag: '🇬🇧', name: 'English', nativeName: 'Ingliz'),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.xxl),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: AppSpacing.xxxl),
              const DisplayTitle('Tilni tanlang', size: 32),
              const SizedBox(height: AppSpacing.sm),
              Text(
                'Ilova va menyu tili',
                style: TextStyle(color: AppColors.textMedium, fontSize: 15),
              ),
              const SizedBox(height: AppSpacing.xxxl),
              Expanded(
                child: Column(
                  children: [
                    for (final opt in _options) ...[
                      _LanguageTile(
                        flag: opt.flag,
                        name: opt.name,
                        nativeName: opt.nativeName,
                        selected: _selected == opt.code,
                        onTap: () => setState(() => _selected = opt.code),
                      ),
                      const SizedBox(height: AppSpacing.md),
                    ],
                  ],
                ),
              ),
              PrimaryButton(
                label: 'Davom etish',
                onPressed: () async {
                  await ref.read(languageProvider.notifier).setLanguage(_selected);
                  if (context.mounted) context.go(AppRoutes.login);
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _LanguageTile extends StatelessWidget {
  const _LanguageTile({
    required this.flag,
    required this.name,
    required this.nativeName,
    required this.selected,
    required this.onTap,
  });

  final String flag;
  final String name;
  final String nativeName;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: selected ? AppColors.creamCard : Colors.white,
      borderRadius: BorderRadius.circular(AppRadius.xl),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.xl),
        child: Container(
          padding: const EdgeInsets.all(AppSpacing.xl),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(AppRadius.xl),
            border: Border.all(
              color: selected ? AppColors.terracotta : Colors.transparent,
              width: 2,
            ),
          ),
          child: Row(
            children: [
              Text(flag, style: const TextStyle(fontSize: 32)),
              const SizedBox(width: AppSpacing.lg),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      name,
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w600,
                        color: AppColors.textDark,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      nativeName,
                      style: const TextStyle(fontSize: 13, color: AppColors.textLight),
                    ),
                  ],
                ),
              ),
              if (selected)
                Container(
                  width: 24,
                  height: 24,
                  decoration: const BoxDecoration(
                    color: AppColors.terracotta,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.check, color: Colors.white, size: 16),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
