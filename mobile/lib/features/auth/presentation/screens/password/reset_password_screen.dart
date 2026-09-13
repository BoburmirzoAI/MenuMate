import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
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

class ResetPasswordScreen extends ConsumerStatefulWidget {
  const ResetPasswordScreen({super.key, this.prefilledEmail});
  final String? prefilledEmail;

  @override
  ConsumerState<ResetPasswordScreen> createState() => _ResetPasswordScreenState();
}

class _ResetPasswordScreenState extends ConsumerState<ResetPasswordScreen> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _email;
  final _code = TextEditingController();
  final _password = TextEditingController();
  final _confirm = TextEditingController();
  bool _saving = false;
  bool _hidePassword = true;

  @override
  void initState() {
    super.initState();
    _email = TextEditingController(text: widget.prefilledEmail ?? '');
  }

  @override
  void dispose() {
    _email.dispose();
    _code.dispose();
    _password.dispose();
    _confirm.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _saving = true);
    try {
      await ref.read(authRepositoryProvider).resetPassword(
            email: _email.text.trim(),
            code: _code.text.trim(),
            newPassword: _password.text,
            newPasswordConfirm: _confirm.text,
          );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(ref.tr('reset_password_success'))),
      );
      context.go(AppRoutes.login);
    } on ApiException catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: SafeArea(
        child: SingleChildScrollView(
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
                  child: const Icon(Icons.mark_email_read_outlined,
                      color: AppColors.terracotta, size: 28),
                ),
                const SizedBox(height: AppSpacing.lg),
                DisplayTitle(ref.tr('reset_password_title'), size: 26),
                const SizedBox(height: AppSpacing.sm),
                Text(
                  ref.tr('reset_password_hint'),
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
                const SizedBox(height: AppSpacing.lg),

                Text(ref.tr('reset_code_label'), style: _labelStyle),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: _code,
                  keyboardType: TextInputType.number,
                  inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                  decoration: const InputDecoration(hintText: '123456'),
                  validator: (v) => v == null || v.length < 4 ? '?' : null,
                ),
                const SizedBox(height: AppSpacing.lg),

                Text(ref.tr('reset_new_password'), style: _labelStyle),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: _password,
                  obscureText: _hidePassword,
                  decoration: InputDecoration(
                    hintText: '••••••••',
                    suffixIcon: IconButton(
                      icon: Icon(_hidePassword ? Icons.visibility_off : Icons.visibility, size: 20),
                      onPressed: () => setState(() => _hidePassword = !_hidePassword),
                    ),
                  ),
                  validator: (v) => v == null || v.length < 8 ? '?' : null,
                ),
                const SizedBox(height: AppSpacing.lg),

                Text(ref.tr('password_confirm'), style: _labelStyle),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: _confirm,
                  obscureText: _hidePassword,
                  decoration: const InputDecoration(hintText: '••••••••'),
                  validator: (v) => v != _password.text ? '?' : null,
                ),

                const SizedBox(height: AppSpacing.xxl),
                PrimaryButton(
                  label: ref.tr('reset_password_cta'),
                  onPressed: _saving ? null : _submit,
                  isLoading: _saving,
                ),
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
