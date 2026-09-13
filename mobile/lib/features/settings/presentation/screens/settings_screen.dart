import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/config/app_config.dart';
import '../../../../core/l10n/language_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/widgets/section_card.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  bool _pushEnabled = true;
  bool _mealReminderEnabled = true;
  bool _holidayNotifEnabled = true;

  static const _languages = [
    (code: 'uz', label: "O'zbekcha", flag: '🇺🇿'),
    (code: 'ru', label: 'Русский', flag: '🇷🇺'),
    (code: 'en', label: 'English', flag: '🇬🇧'),
  ];

  @override
  Widget build(BuildContext context) {
    final currentLang = ref.watch(languageProvider);

    return Scaffold(
      appBar: AppBar(title: Text(ref.tr('settings_title')), centerTitle: false),
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.xxl),
        children: [
          _SectionTitle(ref.tr('settings_section_language')),
          const SizedBox(height: AppSpacing.sm),
          SectionCard(
            color: Colors.white,
            padding: EdgeInsets.zero,
            child: Column(
              children: [
                for (int i = 0; i < _languages.length; i++) ...[
                  _LanguageRow(
                    label: _languages[i].label,
                    flag: _languages[i].flag,
                    selected: currentLang == _languages[i].code,
                    onTap: () => ref
                        .read(languageProvider.notifier)
                        .setLanguage(_languages[i].code),
                  ),
                  if (i != _languages.length - 1) const Divider(height: 1, indent: 56),
                ],
              ],
            ),
          ),

          const SizedBox(height: AppSpacing.xxl),
          _SectionTitle(ref.tr('settings_section_notifications')),
          const SizedBox(height: AppSpacing.sm),
          SectionCard(
            color: Colors.white,
            padding: EdgeInsets.zero,
            child: Column(
              children: [
                _SwitchRow(
                  icon: Icons.notifications_outlined,
                  label: ref.tr('settings_push'),
                  value: _pushEnabled,
                  onChanged: (v) => setState(() => _pushEnabled = v),
                ),
                const Divider(height: 1, indent: 56),
                _SwitchRow(
                  icon: Icons.restaurant_menu,
                  label: ref.tr('settings_meal_reminder'),
                  value: _mealReminderEnabled && _pushEnabled,
                  enabled: _pushEnabled,
                  onChanged: (v) => setState(() => _mealReminderEnabled = v),
                ),
                const Divider(height: 1, indent: 56),
                _SwitchRow(
                  icon: Icons.celebration_outlined,
                  label: ref.tr('settings_holiday_notif'),
                  value: _holidayNotifEnabled && _pushEnabled,
                  enabled: _pushEnabled,
                  onChanged: (v) => setState(() => _holidayNotifEnabled = v),
                ),
              ],
            ),
          ),

          const SizedBox(height: AppSpacing.xxl),
          _SectionTitle(ref.tr('settings_section_about')),
          const SizedBox(height: AppSpacing.sm),
          SectionCard(
            color: Colors.white,
            padding: EdgeInsets.zero,
            child: Column(
              children: [
                _InfoRow(
                  icon: Icons.info_outline,
                  label: ref.tr('settings_version'),
                  value: AppConfig.appVersion,
                ),
                const Divider(height: 1, indent: 56),
                _InfoRow(
                  icon: Icons.dns_outlined,
                  label: ref.tr('settings_server'),
                  value: AppConfig.apiBaseUrl.replaceFirst(RegExp(r'^https?://'), ''),
                ),
              ],
            ),
          ),
          const SizedBox(height: AppSpacing.huge),
        ],
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

class _LanguageRow extends StatelessWidget {
  const _LanguageRow({
    required this.label,
    required this.flag,
    required this.selected,
    required this.onTap,
  });

  final String label;
  final String flag;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: 14),
        child: Row(
          children: [
            Text(flag, style: const TextStyle(fontSize: 22)),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                label,
                style: const TextStyle(
                  fontSize: 15, fontWeight: FontWeight.w600, color: AppColors.textDark,
                ),
              ),
            ),
            if (selected)
              const Icon(Icons.check_circle, color: AppColors.terracotta, size: 22)
            else
              const Icon(Icons.circle_outlined, color: AppColors.textLight, size: 22),
          ],
        ),
      ),
    );
  }
}

class _SwitchRow extends StatelessWidget {
  const _SwitchRow({
    required this.icon,
    required this.label,
    required this.value,
    required this.onChanged,
    this.enabled = true,
  });

  final IconData icon;
  final String label;
  final bool value;
  final ValueChanged<bool> onChanged;
  final bool enabled;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: 8),
      child: Row(
        children: [
          Icon(
            icon, size: 20,
            color: enabled ? AppColors.textMedium : AppColors.textLight,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Text(
              label,
              style: TextStyle(
                fontSize: 15, fontWeight: FontWeight.w600,
                color: enabled ? AppColors.textDark : AppColors.textLight,
              ),
            ),
          ),
          Switch(
            value: value,
            onChanged: enabled ? onChanged : null,
            activeThumbColor: AppColors.terracotta,
          ),
        ],
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  const _InfoRow({required this.icon, required this.label, required this.value});
  final IconData icon;
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: 14),
      child: Row(
        children: [
          Icon(icon, size: 20, color: AppColors.textMedium),
          const SizedBox(width: 16),
          Expanded(
            child: Text(
              label,
              style: const TextStyle(
                fontSize: 15, fontWeight: FontWeight.w600, color: AppColors.textDark,
              ),
            ),
          ),
          Text(value, style: const TextStyle(color: AppColors.textMedium)),
        ],
      ),
    );
  }
}
