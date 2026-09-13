import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/router/app_routes.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/primary_button.dart';
import '../../../../core/widgets/section_card.dart';
import '../../data/family_repository.dart';

/// 3f — Oila yaratish (YAXSHILANGAN).
/// Yuqorida progress bar (1/2), illustratsiya karta + form.
class FamilyCreateScreen extends ConsumerStatefulWidget {
  const FamilyCreateScreen({super.key});

  @override
  ConsumerState<FamilyCreateScreen> createState() => _FamilyCreateScreenState();
}

class _FamilyCreateScreenState extends ConsumerState<FamilyCreateScreen> {
  final _formKey = GlobalKey<FormState>();
  final _familyName = TextEditingController();
  final _city = TextEditingController(text: 'Tashkent');
  bool _loading = false;

  final _cities = const [
    'Tashkent', 'Samarkand', 'Bukhara', 'Namangan',
    'Andijan', 'Fergana', 'Nukus', 'Termez', 'Urgench',
  ];

  @override
  void dispose() {
    _familyName.dispose();
    _city.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      await ref.read(familyRepositoryProvider).createFamily(
            familyName: _familyName.text.trim(),
            city: _city.text.trim(),
          );
      ref.invalidate(myFamilyProvider);
      if (mounted) context.go(AppRoutes.memberAdd);
    } on ApiException catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(e.message)));
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Progress + label
            Padding(
              padding: const EdgeInsets.fromLTRB(
                AppSpacing.xxl, AppSpacing.lg, AppSpacing.xxl, 0,
              ),
              child: Row(
                children: [
                  const _StepDot(active: true),
                  const SizedBox(width: 6),
                  Container(width: 40, height: 3, color: AppColors.terracotta),
                  const SizedBox(width: 6),
                  const _StepDot(active: false),
                  const SizedBox(width: AppSpacing.md),
                  Text(
                    '1 / 2 — Oila',
                    style: TextStyle(fontSize: 13, color: AppColors.textMedium, fontWeight: FontWeight.w500),
                  ),
                ],
              ),
            ),

            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(AppSpacing.xxl),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SizedBox(height: AppSpacing.xl),

                      // Illustration card
                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.symmetric(vertical: AppSpacing.xxxl),
                        decoration: BoxDecoration(
                          color: AppColors.creamCard,
                          borderRadius: BorderRadius.circular(AppRadius.xxl),
                        ),
                        child: Column(
                          children: [
                            const Text('👨‍👩‍👧', style: TextStyle(fontSize: 72)),
                            const SizedBox(height: AppSpacing.md),
                            DisplayTitle(ref.tr('family_create_title'), size: 24),
                            const SizedBox(height: AppSpacing.sm),
                            Text(
                              ref.tr('health_optional_subtitle'),
                              style: const TextStyle(color: AppColors.textMedium, fontSize: 14),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: AppSpacing.xxl),

                      _Label(ref.tr('family_name_label')),
                      const SizedBox(height: AppSpacing.sm),
                      TextFormField(
                        controller: _familyName,
                        decoration: const InputDecoration(hintText: 'Masalan: Sobirjonovlar'),
                        validator: (v) => v == null || v.trim().isEmpty ? 'Kiriting' : null,
                      ),
                      const SizedBox(height: AppSpacing.xl),

                      _Label(ref.tr('family_city_label')),
                      const SizedBox(height: AppSpacing.sm),
                      Text(
                        "Ob-havoga qarab menyu tanlash uchun",
                        style: TextStyle(fontSize: 12, color: AppColors.textLight),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: _cities.map((c) {
                          final selected = _city.text == c;
                          return ChoiceChip(
                            label: Text(c),
                            selected: selected,
                            onSelected: (_) => setState(() => _city.text = c),
                            selectedColor: AppColors.terracotta,
                            labelStyle: TextStyle(
                              color: selected ? Colors.white : AppColors.textDark,
                              fontWeight: FontWeight.w500,
                            ),
                            backgroundColor: AppColors.creamCard,
                            side: BorderSide.none,
                          );
                        }).toList(),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            Padding(
              padding: const EdgeInsets.all(AppSpacing.xxl),
              child: PrimaryButton(
                label: 'Davom etish',
                onPressed: _submit,
                isLoading: _loading,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Label extends StatelessWidget {
  const _Label(this.text);
  final String text;
  @override
  Widget build(BuildContext context) => Text(
        text,
        style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: AppColors.textMedium),
      );
}

class _StepDot extends StatelessWidget {
  const _StepDot({required this.active});
  final bool active;
  @override
  Widget build(BuildContext context) => Container(
        width: 24, height: 24,
        decoration: BoxDecoration(
          color: active ? AppColors.terracotta : AppColors.creamCard,
          borderRadius: BorderRadius.circular(12),
        ),
      );
}
