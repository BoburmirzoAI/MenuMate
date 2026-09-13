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
import '../../../auth/presentation/providers/auth_state.dart';
import '../../data/family_repository.dart';
import '../../domain/family.dart';

/// Oila a'zosi formasi — yangi qo'shish yoki mavjudni tahrirlash.
class MemberAddScreen extends ConsumerStatefulWidget {
  const MemberAddScreen({super.key, this.editing});
  final FamilyMember? editing;

  @override
  ConsumerState<MemberAddScreen> createState() => _MemberAddScreenState();
}

class _MemberAddScreenState extends ConsumerState<MemberAddScreen> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _name;
  late final TextEditingController _age;
  late String _gender;
  late String _avatar;
  late Set<int> _selectedHealthIds;
  bool _saving = false;

  static const _avatarsMale = ['👨', '👦', '👴', '🧑'];
  static const _avatarsFemale = ['👩', '👧', '👵', '🧕'];

  bool get _isEdit => widget.editing != null;

  @override
  void initState() {
    super.initState();
    final m = widget.editing;
    _name = TextEditingController(text: m?.name ?? '');
    _age = TextEditingController(text: m?.age.toString() ?? '');
    _gender = m?.gender ?? 'MALE';
    _avatar = _gender == 'FEMALE' ? _avatarsFemale.first : _avatarsMale.first;
    _selectedHealthIds = {...(m?.healthConditions.map((h) => h.id) ?? const <int>[])};
  }

  @override
  void dispose() {
    _name.dispose();
    _age.dispose();
    super.dispose();
  }

  Future<void> _save({bool addAnother = false}) async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _saving = true);
    try {
      final repo = ref.read(familyRepositoryProvider);
      if (_isEdit) {
        await repo.updateMember(widget.editing!.id, {
          'name': _name.text.trim(),
          'age': int.parse(_age.text.trim()),
          'gender': _gender,
          'health_condition_ids': _selectedHealthIds.toList(),
        });
      } else {
        await repo.createMember(
          name: _name.text.trim(),
          age: int.parse(_age.text.trim()),
          gender: _gender,
          healthConditionIds: _selectedHealthIds.toList(),
        );
      }
      ref.invalidate(familyMembersProvider);

      if (!mounted) return;
      if (addAnother) {
        _formKey.currentState!.reset();
        setState(() {
          _name.clear();
          _age.clear();
          _gender = 'MALE';
          _avatar = _avatarsMale.first;
          _selectedHealthIds.clear();
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("A'zo qo'shildi")),
        );
      } else if (context.canPop()) {
        context.pop();
      } else {
        // Onboarding: birinchi a'zo qo'shilgandan keyin
        await ref.read(authProvider.notifier).refresh();
        if (mounted) context.go(AppRoutes.home);
      }
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
    final healthAsync = ref.watch(healthConditionsProvider(null));
    final avatars = _gender == 'FEMALE' ? _avatarsFemale : _avatarsMale;

    return Scaffold(
      appBar: AppBar(
        title: Text(ref.tr(_isEdit ? 'member_edit_title' : 'member_add_title')),
        centerTitle: false,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(AppSpacing.xxl),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Avatar
                      SectionCard(
                        color: Colors.white,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            _Label(ref.tr('avatar_label')),
                            const SizedBox(height: AppSpacing.md),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: avatars.map((emoji) {
                                final selected = _avatar == emoji;
                                return GestureDetector(
                                  onTap: () => setState(() => _avatar = emoji),
                                  child: Container(
                                    width: 56, height: 56,
                                    decoration: BoxDecoration(
                                      color: selected ? AppColors.terracotta : AppColors.creamBg,
                                      borderRadius: BorderRadius.circular(AppRadius.md),
                                      border: Border.all(
                                        color: selected ? AppColors.terracotta : AppColors.creamCard,
                                        width: 2,
                                      ),
                                    ),
                                    alignment: Alignment.center,
                                    child: Text(emoji, style: const TextStyle(fontSize: 28)),
                                  ),
                                );
                              }).toList(),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),

                      // Ism, yosh, jinsi
                      SectionCard(
                        color: Colors.white,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Expanded(
                                  flex: 2,
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      _Label(ref.tr('name_label')),
                                      const SizedBox(height: AppSpacing.sm),
                                      TextFormField(
                                        controller: _name,
                                        decoration: const InputDecoration(hintText: 'Ali'),
                                        validator: (v) => v == null || v.trim().isEmpty ? '?' : null,
                                      ),
                                    ],
                                  ),
                                ),
                                const SizedBox(width: AppSpacing.md),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      _Label(ref.tr('age_label')),
                                      const SizedBox(height: AppSpacing.sm),
                                      TextFormField(
                                        controller: _age,
                                        keyboardType: TextInputType.number,
                                        decoration: const InputDecoration(hintText: '10'),
                                        validator: (v) {
                                          if (v == null || v.isEmpty) return '?';
                                          final n = int.tryParse(v);
                                          if (n == null || n < 0 || n > 120) return '?';
                                          return null;
                                        },
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: AppSpacing.md),
                            _Label(ref.tr('gender_label')),
                            const SizedBox(height: AppSpacing.sm),
                            Row(
                              children: [
                                _GenderPill(
                                  label: ref.tr('gender_male'),
                                  emoji: '👨',
                                  selected: _gender == 'MALE',
                                  onTap: () => setState(() {
                                    _gender = 'MALE';
                                    _avatar = _avatarsMale.first;
                                  }),
                                ),
                                const SizedBox(width: AppSpacing.sm),
                                _GenderPill(
                                  label: ref.tr('gender_female'),
                                  emoji: '👩',
                                  selected: _gender == 'FEMALE',
                                  onTap: () => setState(() {
                                    _gender = 'FEMALE';
                                    _avatar = _avatarsFemale.first;
                                  }),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: AppSpacing.xxl),
                      _SectionTitle(ref.tr('health_optional_title')),
                      const SizedBox(height: 4),
                      Padding(
                        padding: const EdgeInsets.only(left: 4),
                        child: Text(
                          ref.tr('health_optional_subtitle'),
                          style: TextStyle(fontSize: 12, color: AppColors.textLight),
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),

                      healthAsync.when(
                        loading: () => const Padding(
                          padding: EdgeInsets.all(AppSpacing.xl),
                          child: Center(child: CircularProgressIndicator()),
                        ),
                        error: (e, _) => Text(e is ApiException ? e.message : ref.tr('error'), style: const TextStyle(color: AppColors.error)),
                        data: (conditions) => _HealthCategories(
                          conditions: conditions,
                          selectedIds: _selectedHealthIds,
                          onToggle: (id) => setState(() {
                            if (_selectedHealthIds.contains(id)) {
                              _selectedHealthIds.remove(id);
                            } else {
                              _selectedHealthIds.add(id);
                            }
                          }),
                        ),
                      ),

                      const SizedBox(height: AppSpacing.xxl),
                    ],
                  ),
                ),
              ),
            ),

            // Actions
            Padding(
              padding: const EdgeInsets.fromLTRB(
                AppSpacing.xxl, AppSpacing.md, AppSpacing.xxl, AppSpacing.xxl,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  PrimaryButton(
                    label: ref.tr(_isEdit ? 'save' : 'add'),
                    onPressed: _saving ? null : _save,
                    isLoading: _saving,
                  ),
                  if (!_isEdit) ...[
                    const SizedBox(height: AppSpacing.sm),
                    SecondaryButton(
                      label: ref.tr('add_and_more'),
                      icon: Icons.add,
                      onPressed: _saving ? null : () => _save(addAnother: true),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================================
// Kasallik kategoriyalari — collapsible (xarid ekranidagi kabi)
// ============================================================================

class _HealthCategories extends ConsumerWidget {
  const _HealthCategories({
    required this.conditions,
    required this.selectedIds,
    required this.onToggle,
  });

  final List<HealthCondition> conditions;
  final Set<int> selectedIds;
  final void Function(int id) onToggle;

  static const _categoryMeta = {
    'ALLERGY': ('🌾', 'health_cat_allergy', Color(0xFFCF6B32)),
    'DIABETES': ('💉', 'health_cat_diabetes', Color(0xFF89A9C4)),
    'HEART': ('❤️', 'health_cat_heart', Color(0xFFB84C3A)),
    'OBESITY': ('⚖️', 'health_cat_obesity', Color(0xFF7BA05B)),
    'OTHER': ('📋', 'health_cat_other', Color(0xFFE0A93A)),
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final grouped = <String, List<HealthCondition>>{};
    for (final c in conditions) {
      grouped.putIfAbsent(c.category, () => []).add(c);
    }

    return Column(
      children: grouped.entries.map((entry) {
        final meta = _categoryMeta[entry.key] ?? ('•', 'cat_other', AppColors.textLight);
        final selectedInCategory = entry.value
            .where((c) => selectedIds.contains(c.id))
            .length;
        return Padding(
          padding: const EdgeInsets.only(bottom: AppSpacing.md),
          child: _HealthCategoryTile(
            emoji: meta.$1,
            label: ref.tr(meta.$2),
            color: meta.$3,
            total: entry.value.length,
            selected: selectedInCategory,
            conditions: entry.value,
            selectedIds: selectedIds,
            onToggle: onToggle,
          ),
        );
      }).toList(),
    );
  }
}

class _HealthCategoryTile extends ConsumerStatefulWidget {
  const _HealthCategoryTile({
    required this.emoji,
    required this.label,
    required this.color,
    required this.total,
    required this.selected,
    required this.conditions,
    required this.selectedIds,
    required this.onToggle,
  });

  final String emoji;
  final String label;
  final Color color;
  final int total;
  final int selected;
  final List<HealthCondition> conditions;
  final Set<int> selectedIds;
  final void Function(int id) onToggle;

  @override
  ConsumerState<_HealthCategoryTile> createState() => _HealthCategoryTileState();
}

class _HealthCategoryTileState extends ConsumerState<_HealthCategoryTile> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return SectionCard(
      color: Colors.white,
      padding: EdgeInsets.zero,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          InkWell(
            onTap: () => setState(() => _expanded = !_expanded),
            borderRadius: BorderRadius.circular(AppRadius.lg),
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: _expanded ? AppColors.creamCard : Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: const Radius.circular(AppRadius.lg),
                  topRight: const Radius.circular(AppRadius.lg),
                  bottomLeft: Radius.circular(_expanded ? 0 : AppRadius.lg),
                  bottomRight: Radius.circular(_expanded ? 0 : AppRadius.lg),
                ),
              ),
              child: Row(
                children: [
                  Container(
                    width: 42, height: 42,
                    decoration: BoxDecoration(
                      color: widget.color,
                      borderRadius: BorderRadius.circular(AppRadius.sm),
                    ),
                    alignment: Alignment.center,
                    child: Text(widget.emoji, style: const TextStyle(fontSize: 20)),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          widget.label,
                          style: const TextStyle(
                            fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.textDark,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          '${widget.total} ${ref.tr('health_variants_selected').replaceAll('N', widget.selected.toString())}',
                          style: const TextStyle(fontSize: 12, color: AppColors.textLight),
                        ),
                      ],
                    ),
                  ),
                  if (widget.selected > 0)
                    Container(
                      margin: const EdgeInsets.only(right: 4),
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: AppColors.terracotta,
                        borderRadius: BorderRadius.circular(AppRadius.pill),
                      ),
                      child: Text(
                        '${widget.selected}',
                        style: const TextStyle(
                          fontSize: 11, fontWeight: FontWeight.w700, color: Colors.white,
                        ),
                      ),
                    ),
                  Icon(
                    _expanded ? Icons.expand_less : Icons.chevron_right,
                    color: AppColors.textLight,
                  ),
                ],
              ),
            ),
          ),
          if (_expanded)
            Padding(
              padding: const EdgeInsets.all(AppSpacing.md),
              child: Wrap(
                spacing: 8,
                runSpacing: 8,
                children: widget.conditions.map((c) {
                  final selected = widget.selectedIds.contains(c.id);
                  return _HealthChip(
                    label: c.name,
                    selected: selected,
                    onTap: () => widget.onToggle(c.id),
                  );
                }).toList(),
              ),
            ),
        ],
      ),
    );
  }
}

class _HealthChip extends StatelessWidget {
  const _HealthChip({required this.label, required this.selected, required this.onTap});
  final String label;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: selected ? AppColors.terracotta : AppColors.creamBg,
          borderRadius: BorderRadius.circular(AppRadius.pill),
          border: Border.all(
            color: selected ? AppColors.terracotta : AppColors.creamCard,
          ),
        ),
        child: Text(
          label,
          style: TextStyle(
            color: selected ? Colors.white : AppColors.textDark,
            fontWeight: FontWeight.w600,
            fontSize: 13,
          ),
        ),
      ),
    );
  }
}

// ============================================================================
// Reusable widgets
// ============================================================================

class _GenderPill extends StatelessWidget {
  const _GenderPill({
    required this.label,
    required this.emoji,
    required this.selected,
    required this.onTap,
  });

  final String label;
  final String emoji;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: selected ? AppColors.terracotta : AppColors.creamBg,
            borderRadius: BorderRadius.circular(AppRadius.lg),
            border: Border.all(
              color: selected ? AppColors.terracotta : AppColors.creamCard,
            ),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(emoji, style: const TextStyle(fontSize: 20)),
              const SizedBox(width: 8),
              Text(
                label,
                style: TextStyle(
                  color: selected ? Colors.white : AppColors.textDark,
                  fontSize: 15,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
        ),
      ),
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

class _Label extends StatelessWidget {
  const _Label(this.text);
  final String text;
  @override
  Widget build(BuildContext context) => Text(
        text,
        style: const TextStyle(
          fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textMedium,
        ),
      );
}
