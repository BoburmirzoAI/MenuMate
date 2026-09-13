import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../storage/preferences.dart';
import 'app_strings.dart';

/// Joriy tilni saqlovchi provider.
/// UI'da til o'zgarganda watch qilgan barcha widget qayta chiziladi.
class LanguageNotifier extends Notifier<String> {
  @override
  String build() {
    final prefs = ref.watch(preferencesProvider);
    return prefs.getLanguage();
  }

  Future<void> setLanguage(String lang) async {
    if (!['uz', 'ru', 'en'].contains(lang)) return;
    final prefs = ref.read(preferencesProvider);
    await prefs.setLanguage(lang);
    state = lang;
  }
}

final languageProvider = NotifierProvider<LanguageNotifier, String>(
  LanguageNotifier.new,
);

/// Tarjima helper — widget'larda `ref.tr('login')` kabi ishlatiladi.
extension TranslateRef on WidgetRef {
  String tr(String key) {
    final lang = watch(languageProvider);
    return AppStrings.t(key, lang);
  }
}
