import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../../core/api/api_exception.dart';
import '../../../../../core/l10n/language_provider.dart';
import '../../../../../core/router/app_routes.dart';
import '../../../../../core/theme/app_colors.dart';
import '../../../../../core/theme/app_spacing.dart';
import '../../../../../core/widgets/primary_button.dart';
import '../../../../../core/widgets/section_card.dart';
import '../../../data/auth_repository.dart';

class ForgotPasswordScreen extends ConsumerStatefulWidget {
  const ForgotPasswordScreen({super.key});

  @override
  ConsumerState<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends ConsumerState<ForgotPasswordScreen> {
  final _formKey = GlobalKey<FormState>();
  final _email = TextEditingController();
  bool _sending = false;

  @override
  void dispose() {
    _email.dispose();
    super.dispose();
  }

  Future<void> _send() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _sending = true);
    try {
      await ref.read(authRepositoryProvider).forgotPassword(_email.text.trim());
      if (!mounted) return;
      context.go(AppRoutes.resetPassword, extra: _email.text.trim());
    } on ApiException catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
    } finally {
      if (mounted) setState(() => _sending = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.xxl),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 56, height: 56,
                  decoration: BoxDecoration(
                    color: AppColors.terracotta.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(AppRadius.md),
                  ),
                  alignment: Alignment.center,
                  child: const Icon(Icons.lock_reset, color: AppColors.terracotta, size: 28),
                ),
                const SizedBox(height: AppSpacing.lg),
                DisplayTitle(ref.tr('forgot_password'), size: 26),
                const SizedBox(height: AppSpacing.sm),
                Text(
                  ref.tr('forgot_password_hint'),
                  style: const TextStyle(color: AppColors.textMedium, fontSize: 14, height: 1.4),
                ),
                const SizedBox(height: AppSpacing.xxl),
                Text(ref.tr('email'), style: _labelStyle),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: _email,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(hintText: 'user@example.com'),
                  validator: (v) => v == null || !v.contains('@') ? 'email' : null,
                ),
                const Spacer(),
                PrimaryButton(
                  label: ref.tr('forgot_send_code'),
                  onPressed: _sending ? null : _send,
                  isLoading: _sending,
                ),
                const SizedBox(height: AppSpacing.md),
              ],
            ),
          ),
        ),
      ),
    );
  }

  static const _labelStyle = TextStyle(
    fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textMedium,
  );
}
