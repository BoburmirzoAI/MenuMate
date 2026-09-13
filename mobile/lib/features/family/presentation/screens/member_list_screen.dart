import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/router/app_routes.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/section_card.dart';
import '../../../../core/widgets/state_views.dart';
import '../../data/family_repository.dart';
import '../../domain/family.dart';

/// Oila a'zolarining ro'yxati — tahrirlash va o'chirish uchun.
class MemberListScreen extends ConsumerWidget {
  const MemberListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final membersAsync = ref.watch(familyMembersProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text(ref.tr('family_members_title')),
        centerTitle: false,
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.push(AppRoutes.memberAdd),
        icon: const Icon(Icons.add),
        label: Text(ref.tr('member_add_button')),
        backgroundColor: AppColors.terracotta,
        foregroundColor: Colors.white,
      ),
      body: membersAsync.when(
        loading: () => const LoadingView(),
        error: (err, _) => ErrorRetryView(
          message: err is ApiException ? err.message : ref.tr('error'),
          onRetry: () => ref.invalidate(familyMembersProvider),
        ),
        data: (members) {
          if (members.isEmpty) return _EmptyView(onAdd: () => context.push(AppRoutes.memberAdd));
          return ListView.separated(
            padding: const EdgeInsets.fromLTRB(
              AppSpacing.xxl, AppSpacing.md, AppSpacing.xxl, 100,
            ),
            itemCount: members.length,
            separatorBuilder: (_, _) => const SizedBox(height: AppSpacing.md),
            itemBuilder: (context, i) => _MemberCard(
              member: members[i],
              onTap: () => context.push('/family/members/${members[i].id}/edit'),
              onDelete: () => _confirmDelete(context, ref, members[i]),
            ),
          );
        },
      ),
    );
  }

  Future<void> _confirmDelete(
    BuildContext context, WidgetRef ref, FamilyMember m,
  ) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text("${m.name}ni o'chirish?"),
        content: const Text("A'zo va uning ma'lumotlari butunlay o'chiriladi."),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(dialogContext).pop(false),
            child: const Text('Bekor'),
          ),
          TextButton(
            onPressed: () => Navigator.of(dialogContext).pop(true),
            child: const Text("O'chirish"),
          ),
        ],
      ),
    );
    if (ok != true) return;
    try {
      await ref.read(familyRepositoryProvider).deleteMember(m.id);
      ref.invalidate(familyMembersProvider);
    } on ApiException catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
      }
    }
  }
}

class _MemberCard extends ConsumerWidget {
  const _MemberCard({
    required this.member,
    required this.onTap,
    required this.onDelete,
  });

  final FamilyMember member;
  final VoidCallback onTap;
  final VoidCallback onDelete;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return SectionCard(
      color: Colors.white,
      onTap: onTap,
      child: Row(
        children: [
          Container(
            width: 52, height: 52,
            decoration: BoxDecoration(
              color: AppColors.creamCard,
              borderRadius: BorderRadius.circular(AppRadius.md),
            ),
            alignment: Alignment.center,
            child: Text(
              member.gender == 'FEMALE' ? '👩' : '👨',
              style: const TextStyle(fontSize: 26),
            ),
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  member.name,
                  style: const TextStyle(
                    fontSize: 16, fontWeight: FontWeight.w700, color: AppColors.textDark,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  '${member.age} ${ref.tr('years_old')} · ${member.gender == 'FEMALE' ? ref.tr('gender_female') : ref.tr('gender_male')}',
                  style: const TextStyle(fontSize: 12, color: AppColors.textLight),
                ),
                if (member.healthConditions.isNotEmpty) ...[
                  const SizedBox(height: 6),
                  Wrap(
                    spacing: 4,
                    runSpacing: 4,
                    children: member.healthConditions.take(3).map((h) {
                      return Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: AppColors.warning.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(AppRadius.pill),
                        ),
                        child: Text(
                          h.name,
                          style: const TextStyle(
                            fontSize: 10, fontWeight: FontWeight.w600, color: AppColors.textDark,
                          ),
                        ),
                      );
                    }).toList(),
                  ),
                  if (member.healthConditions.length > 3)
                    Padding(
                      padding: const EdgeInsets.only(top: 3),
                      child: Text(
                        '+${member.healthConditions.length - 3} ta',
                        style: const TextStyle(fontSize: 11, color: AppColors.textLight),
                      ),
                    ),
                ],
              ],
            ),
          ),
          IconButton(
            icon: const Icon(Icons.delete_outline, color: AppColors.error, size: 22),
            onPressed: onDelete,
            tooltip: ref.tr('delete'),
          ),
        ],
      ),
    );
  }
}

class _EmptyView extends ConsumerWidget {
  const _EmptyView({required this.onAdd});
  final VoidCallback onAdd;

  @override
  Widget build(BuildContext context, WidgetRef ref) => EmptyView(
        emoji: '👨‍👩‍👧',
        title: ref.tr('family_no_members_title'),
        subtitle: ref.tr('family_no_members_body'),
        ctaLabel: ref.tr('member_add_button'),
        onCta: onAdd,
      );
}
