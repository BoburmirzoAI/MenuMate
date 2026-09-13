import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Oddiy sozlamalar (til, tema va h.k.).
class Preferences {
  Preferences(this._prefs);

  final SharedPreferences _prefs;

  static const _kLanguage = 'language';
  static const _kOnboardingSeen = 'onboarding_seen';
  static const _kThemeMode = 'theme_mode';

  String getLanguage() => _prefs.getString(_kLanguage) ?? 'uz';
  Future<bool> setLanguage(String lang) => _prefs.setString(_kLanguage, lang);

  bool getOnboardingSeen() => _prefs.getBool(_kOnboardingSeen) ?? false;
  Future<bool> setOnboardingSeen(bool value) =>
      _prefs.setBool(_kOnboardingSeen, value);

  String getThemeMode() => _prefs.getString(_kThemeMode) ?? 'system';
  Future<bool> setThemeMode(String mode) => _prefs.setString(_kThemeMode, mode);
}

/// SharedPreferences instance — async, main.dart'da initialize qilinadi.
final sharedPreferencesProvider = Provider<SharedPreferences>((ref) {
  throw UnimplementedError(
    'sharedPreferencesProvider main.dart\'da override qilinishi kerak',
  );
});

final preferencesProvider = Provider<Preferences>((ref) {
  return Preferences(ref.watch(sharedPreferencesProvider));
});
