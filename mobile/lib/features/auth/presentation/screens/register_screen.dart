import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/primary_button.dart';
import '../../../../core/widgets/section_card.dart';
import '../providers/auth_state.dart';

/// 3e — Ro'yxatdan o'tish.
class RegisterScreen extends ConsumerStatefulWidget {
  const RegisterScreen({super.key});

  @override
  ConsumerState<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends ConsumerState<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _firstNameCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  final _confirmCtrl = TextEditingController();
  bool _passwordVisible = false;

  @override
  void dispose() {
    _firstNameCtrl.dispose();
    _emailCtrl.dispose();
    _passwordCtrl.dispose();
    _confirmCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    final lang = ref.read(languageProvider);
    await ref.read(authProvider.notifier).register(
          email: _emailCtrl.text.trim(),
          password: _passwordCtrl.text,
          passwordConfirm: _confirmCtrl.text,
          firstName: _firstNameCtrl.text.trim().isEmpty ? null : _firstNameCtrl.text.trim(),
          language: lang.toUpperCase(),
        );
    if (!mounted) return;
    final state = ref.read(authProvider);
    if (state.hasError) {
      final err = state.error;
      final msg = err is ApiException ? err.message : 'Xatolik yuz berdi';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
    }
  }

  @override
  Widget build(BuildContext context) {
    final isLoading = ref.watch(authProvider).isLoading;

    return Scaffold(
      appBar: AppBar(leading: const BackButton()),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.xxl),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const DisplayTitle("Ro'yxatdan o'tish", size: 32),
                const SizedBox(height: AppSpacing.sm),
                Text(
                  "Yangi akkaunt yarating",
                  style: TextStyle(color: AppColors.textMedium, fontSize: 15),
                ),
                const SizedBox(height: AppSpacing.xxxl),

                const _Label('Ism'),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: _firstNameCtrl,
                  decoration: const InputDecoration(hintText: 'Bobur'),
                ),
                const SizedBox(height: AppSpacing.lg),

                const _Label('Email'),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: _emailCtrl,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(hintText: 'siz@example.com'),
                  validator: (v) => v == null || !v.contains('@') ? 'Email noto\'g\'ri' : null,
                ),
                const SizedBox(height: AppSpacing.lg),

                const _Label('Parol'),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: _passwordCtrl,
                  obscureText: !_passwordVisible,
                  decoration: InputDecoration(
                    hintText: 'Kamida 8 belgi',
                    suffixIcon: IconButton(
                      icon: Icon(_passwordVisible ? Icons.visibility_off : Icons.visibility),
                      onPressed: () => setState(() => _passwordVisible = !_passwordVisible),
                    ),
                  ),
                  validator: (v) => v == null || v.length < 8 ? 'Kamida 8 belgi' : null,
                ),
                const SizedBox(height: AppSpacing.lg),

                const _Label('Parolni takrorlang'),
                const SizedBox(height: AppSpacing.sm),
                TextFormField(
                  controller: _confirmCtrl,
                  obscureText: !_passwordVisible,
                  decoration: const InputDecoration(hintText: '••••••••'),
                  validator: (v) => v != _passwordCtrl.text ? 'Parollar mos emas' : null,
                ),
                const SizedBox(height: AppSpacing.huge),

                PrimaryButton(
                  label: "Ro'yxatdan o'tish",
                  onPressed: _submit,
                  isLoading: isLoading,
                ),
                const SizedBox(height: AppSpacing.xl),

                Center(
                  child: TextButton(
                    onPressed: () => context.pop(),
                    child: const Text('Akkauntingiz bormi? Kirish'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _Label extends StatelessWidget {
  const _Label(this.text);
  final String text;

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: AppColors.textMedium),
    );
  }
}
