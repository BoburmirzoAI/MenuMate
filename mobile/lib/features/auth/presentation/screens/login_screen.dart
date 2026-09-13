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
import '../providers/auth_state.dart';

/// 3d — Kirish (Login).
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  bool _passwordVisible = false;

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passwordCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    await ref.read(authProvider.notifier).login(
          email: _emailCtrl.text.trim(),
          password: _passwordCtrl.text,
        );
    if (!mounted) return;
    // Muvaffaqiyat bo'lsa — router auto-redirect qiladi.
    // Xato bo'lsa SnackBar ko'rsatamiz.
    final state = ref.read(authProvider);
    if (state.hasError) {
      final err = state.error;
      final msg = err is ApiException ? err.message : 'Xatolik yuz berdi';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
    }
  }

  @override
  Widget build(BuildContext context) {
    final authAsync = ref.watch(authProvider);
    final isLoading = authAsync.isLoading;

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.xxl),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: AppSpacing.xxxl),
                  // Logo
                  Container(
                    width: 72, height: 72,
                    decoration: BoxDecoration(
                      color: AppColors.creamCard,
                      borderRadius: BorderRadius.circular(AppRadius.xl),
                    ),
                    alignment: Alignment.center,
                    child: const Text('🍽️', style: TextStyle(fontSize: 36)),
                  ),
                  const SizedBox(height: AppSpacing.xxl),
                  const DisplayTitle('Xush kelibsiz', size: 36),
                  const SizedBox(height: AppSpacing.sm),
                  Text(
                    "Menu Mate akkauntingizga kiring",
                    style: TextStyle(color: AppColors.textMedium, fontSize: 15),
                  ),
                  const SizedBox(height: AppSpacing.huge),

                  // Email
                  const _Label('Email'),
                  const SizedBox(height: AppSpacing.sm),
                  TextFormField(
                    controller: _emailCtrl,
                    keyboardType: TextInputType.emailAddress,
                    decoration: const InputDecoration(hintText: 'siz@example.com'),
                    validator: (v) => v == null || !v.contains('@') ? 'Email noto\'g\'ri' : null,
                  ),
                  const SizedBox(height: AppSpacing.xl),

                  // Parol
                  const _Label('Parol'),
                  const SizedBox(height: AppSpacing.sm),
                  TextFormField(
                    controller: _passwordCtrl,
                    obscureText: !_passwordVisible,
                    decoration: InputDecoration(
                      hintText: '••••••••',
                      suffixIcon: IconButton(
                        icon: Icon(_passwordVisible ? Icons.visibility_off : Icons.visibility),
                        onPressed: () => setState(() => _passwordVisible = !_passwordVisible),
                      ),
                    ),
                    validator: (v) => v == null || v.length < 8 ? 'Kamida 8 belgi' : null,
                  ),
                  const SizedBox(height: AppSpacing.md),

                  Align(
                    alignment: Alignment.centerRight,
                    child: TextButton(
                      onPressed: () => context.push(AppRoutes.forgotPassword),
                      child: Text(ref.tr('forgot_password')),
                    ),
                  ),
                  const SizedBox(height: AppSpacing.xl),

                  PrimaryButton(
                    label: 'Kirish',
                    onPressed: _submit,
                    isLoading: isLoading,
                  ),
                  const SizedBox(height: AppSpacing.xl),

                  // Register link
                  Center(
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          "Akkauntingiz yo'qmi? ",
                          style: TextStyle(color: AppColors.textMedium),
                        ),
                        TextButton(
                          style: TextButton.styleFrom(padding: EdgeInsets.zero),
                          onPressed: () => context.push(AppRoutes.register),
                          child: const Text("Ro'yxatdan o'ting"),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
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
      style: const TextStyle(
        fontSize: 13,
        fontWeight: FontWeight.w600,
        color: AppColors.textMedium,
      ),
    );
  }
}
