import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/router/app_routes.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/section_card.dart';
import '../../../../core/api/api_exception.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/widgets/app_bottom_sheet.dart';
import '../../../../core/widgets/app_dialog.dart';
import '../../../auth/presentation/providers/auth_state.dart';
import '../../../family/data/family_repository.dart';
import '../../../family/domain/family.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authProvider).value;
    final user = (auth is AuthAuthenticated) ? auth.user : null;
    final family = ref.watch(myFamilyProvider).value;
    final members = ref.watch(familyMembersProvider).value ?? const [];

    return Scaffold(
      appBar: AppBar(title: Text(ref.tr('profile_title')), centerTitle: false),
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.xxl),
        children: [
          _ProfileHeader(user: user),
          const SizedBox(height: AppSpacing.xxl),

          _SectionTitle(ref.tr('profile_section_family')),
          const SizedBox(height: AppSpacing.sm),
          SectionCard(
            color: Colors.white,
            padding: EdgeInsets.zero,
            child: Column(
              children: [
                _Row(
                  icon: Icons.family_restroom,
                  label: ref.tr('profile_family_name'),
                  value: family?.familyName ?? '—',
                  onTap: family == null
                      ? null
                      : () => _editFamilyName(context, ref, family),
                ),
                const Divider(height: 1, indent: 56),
                _Row(
                  icon: Icons.location_on_outlined,
                  label: ref.tr('profile_city'),
                  value: family?.city ?? '—',
                  onTap: family == null
                      ? null
                      : () => _editCity(context, ref, family),
                ),
                const Divider(height: 1, indent: 56),
                _Row(
                  icon: Icons.groups_outlined,
                  label: ref.tr('profile_members'),
                  value: '${members.length} ${ref.tr('profile_members_count_suffix')}',
                  onTap: () => context.push(AppRoutes.memberList),
                ),
              ],
            ),
          ),

          const SizedBox(height: AppSpacing.xxl),
          _SectionTitle(ref.tr('profile_section_app')),
          const SizedBox(height: AppSpacing.sm),
          SectionCard(
            color: Colors.white,
            padding: EdgeInsets.zero,
            child: Column(
              children: [
                _Row(
                  icon: Icons.settings_outlined,
                  label: ref.tr('profile_settings'),
                  onTap: () => context.push(AppRoutes.settings),
                ),
                const Divider(height: 1, indent: 56),
                _Row(
                  icon: Icons.notifications_outlined,
                  label: ref.tr('profile_notifications'),
                  onTap: () => context.push(AppRoutes.notifications),
                ),
              ],
            ),
          ),

          const SizedBox(height: AppSpacing.xxl),
          _SectionTitle(ref.tr('profile_section_account')),
          const SizedBox(height: AppSpacing.sm),
          SectionCard(
            color: Colors.white,
            padding: EdgeInsets.zero,
            child: Column(
              children: [
                _Row(
                  icon: Icons.logout,
                  label: ref.tr('logout'),
                  onTap: () => _confirmLogout(context, ref),
                ),
                const Divider(height: 1, indent: 56),
                _Row(
                  icon: Icons.delete_outline,
                  label: ref.tr('profile_delete_account'),
                  iconColor: AppColors.error,
                  labelColor: AppColors.error,
                  onTap: () => _confirmDelete(context, ref),
                ),
              ],
            ),
          ),
          const SizedBox(height: AppSpacing.huge),
        ],
      ),
    );
  }

  Future<void> _editFamilyName(
    BuildContext context, WidgetRef ref, FamilyProfile family,
  ) async {
    final ctrl = TextEditingController(text: family.familyName);
    final newName = await AppDialog.show<String>(
      context: context,
      dialog: AppDialog(
        title: ref.tr('profile_family_name'),
        subtitle: ref.tr('profile_family_name_subtitle'),
        icon: Icons.family_restroom,
        confirmLabel: ref.tr('save'),
        onConfirm: () {
          final v = ctrl.text.trim();
          Navigator.of(context).pop(v.isEmpty ? null : v);
        },
        child: TextField(
          controller: ctrl,
          autofocus: true,
          decoration: const InputDecoration(hintText: 'Sobirjanovlar'),
        ),
      ),
    );
    if (newName == null || newName == family.familyName) return;
    if (!context.mounted) return;
    await _updateFamily(context, ref, {'family_name': newName});
  }

  Future<void> _editCity(
    BuildContext context, WidgetRef ref, FamilyProfile family,
  ) async {
    const cities = [
      'Tashkent', 'Samarkand', 'Bukhara', 'Namangan',
      'Andijan', 'Fergana', 'Nukus', 'Termez', 'Urgench',
    ];
    final picked = await AppBottomSheet.show<String>(
      context: context,
      title: ref.tr('profile_city_pick_title'),
      subtitle: ref.tr('profile_city_pick_sub'),
      child: Wrap(
        spacing: 8, runSpacing: 8,
        children: cities.map((c) {
          final selected = c == family.city;
          return GestureDetector(
            onTap: () => Navigator.of(context).pop(c),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: selected ? AppColors.terracotta : Colors.white,
                borderRadius: BorderRadius.circular(AppRadius.pill),
                border: Border.all(
                  color: selected ? AppColors.terracotta : AppColors.creamCard,
                  width: 1.5,
                ),
              ),
              child: Text(
                c,
                style: TextStyle(
                  color: selected ? Colors.white : AppColors.textDark,
                  fontWeight: FontWeight.w700,
                  fontSize: 14,
                ),
              ),
            ),
          );
        }).toList(),
      ),
    );
    if (picked == null || picked == family.city) return;
    if (!context.mounted) return;
    await _updateFamily(context, ref, {'city': picked});
  }

  Future<void> _updateFamily(
    BuildContext context, WidgetRef ref, Map<String, dynamic> fields,
  ) async {
    try {
      await ref.read(familyRepositoryProvider).updateFamily(fields);
      ref.invalidate(myFamilyProvider);
    } on ApiException catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
    }
  }

  Future<void> _confirmLogout(BuildContext context, WidgetRef ref) async {
    final ok = await AppDialog.show<bool>(
      context: context,
      dialog: AppDialog(
        title: ref.tr('logout_confirm_title'),
        icon: Icons.logout,
        confirmLabel: ref.tr('logout'),
        destructive: true,
        onConfirm: () => Navigator.of(context).pop(true),
        child: Text(
          ref.tr('logout_confirm_body'),
          style: TextStyle(color: AppColors.textMedium, fontSize: 14),
        ),
      ),
    );
    if (ok != true) return;
    await ref.read(authProvider.notifier).logout();
  }

  Future<void> _confirmDelete(BuildContext context, WidgetRef ref) async {
    final passwordCtrl = TextEditingController();
    final formKey = GlobalKey<FormState>();
    bool submitting = false;

    final confirmed = await AppDialog.show<bool>(
      context: context,
      dialog: StatefulBuilder(
        builder: (dialogCtx, setLocal) => AppDialog(
          title: ref.tr('delete_account_title'),
          icon: Icons.delete_outline,
          iconColor: AppColors.error,
          destructive: true,
          confirmLabel: ref.tr('delete_account_cta'),
          confirmLoading: submitting,
          onConfirm: () async {
            if (!formKey.currentState!.validate()) return;
            setLocal(() => submitting = true);
            try {
              await ref.read(authProvider.notifier)
                  .deleteAccount(password: passwordCtrl.text);
              if (dialogCtx.mounted) Navigator.of(dialogCtx).pop(true);
            } on ApiException catch (e) {
              setLocal(() => submitting = false);
              if (dialogCtx.mounted) {
                ScaffoldMessenger.of(dialogCtx).showSnackBar(
                  SnackBar(content: Text(e.message)),
                );
              }
            }
          },
          child: Form(
            key: formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  ref.tr('delete_account_body'),
                  style: const TextStyle(
                    fontSize: 13, color: AppColors.textMedium, height: 1.4,
                  ),
                ),
                const SizedBox(height: AppSpacing.lg),
                TextFormField(
                  controller: passwordCtrl,
                  obscureText: true,
                  autofocus: true,
                  decoration: InputDecoration(
                    hintText: ref.tr('delete_password_hint'),
                    prefixIcon: const Icon(Icons.lock_outline, size: 20),
                  ),
                  validator: (v) => v == null || v.isEmpty
                      ? ref.tr('delete_password_required') : null,
                ),
              ],
            ),
          ),
        ),
      ),
    );
    passwordCtrl.dispose();
    if (confirmed == true && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(ref.tr('profile_delete_account'))),
      );
    }
  }
}

class _ProfileHeader extends StatelessWidget {
  const _ProfileHeader({required this.user});
  final dynamic user;

  String get _fullName {
    if (user == null) return 'Foydalanuvchi';
    final f = user.firstName ?? '';
    final l = user.lastName ?? '';
    final full = '$f $l'.trim();
    return full.isEmpty ? 'Foydalanuvchi' : full;
  }

  String get _initials {
    final trimmed = _fullName.trim();
    final parts = trimmed.split(RegExp(r'\s+'));
    if (parts.length == 1) return parts.first.characters.first.toUpperCase();
    return (parts.first.characters.first + parts.last.characters.first).toUpperCase();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          width: 88, height: 88,
          decoration: const BoxDecoration(
            color: AppColors.terracotta, shape: BoxShape.circle,
          ),
          alignment: Alignment.center,
          child: Text(
            _initials,
            style: const TextStyle(
              color: Colors.white, fontSize: 30, fontWeight: FontWeight.w700,
            ),
          ),
        ),
        const SizedBox(height: AppSpacing.md),
        DisplayTitle(_fullName, size: 22),
        if (user?.email != null) ...[
          const SizedBox(height: 2),
          Text(
            user.email,
            style: TextStyle(color: AppColors.textMedium, fontSize: 13),
          ),
        ],
      ],
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.title);
  final String title;
  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(left: 4),
        child: Text(
          title.toUpperCase(),
          style: const TextStyle(
            fontSize: 11, fontWeight: FontWeight.w700,
            color: AppColors.textLight, letterSpacing: 0.8,
          ),
        ),
      );
}

class _Row extends StatelessWidget {
  const _Row({
    required this.icon,
    required this.label,
    this.value,
    this.onTap,
    this.iconColor,
    this.labelColor,
  });

  final IconData icon;
  final String label;
  final String? value;
  final VoidCallback? onTap;
  final Color? iconColor;
  final Color? labelColor;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: 14),
        child: Row(
          children: [
            Icon(icon, size: 20, color: iconColor ?? AppColors.textMedium),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                label,
                style: TextStyle(
                  fontSize: 15, fontWeight: FontWeight.w600,
                  color: labelColor ?? AppColors.textDark,
                ),
              ),
            ),
            if (value != null)
              Text(
                value!,
                style: const TextStyle(fontSize: 14, color: AppColors.textMedium),
              ),
            if (onTap != null)
              const Icon(Icons.chevron_right, size: 20, color: AppColors.textLight),
          ],
        ),
      ),
    );
  }
}
