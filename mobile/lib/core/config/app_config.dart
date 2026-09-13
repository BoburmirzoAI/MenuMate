/// Ilova sozlamalari — API URL, versiya va h.k.
///
/// Production'da bu qiymatlar `--dart-define` orqali build vaqtida beriladi:
///   flutter run --dart-define=API_BASE_URL=https://api.menumate.uz
class AppConfig {
  AppConfig._();

  /// Backend API base URL.
  /// - Real telefon (bir Wi-Fi'da) → kompyuter IP: http://192.168.1.105:8000
  /// - Chrome / iOS Simulator → http://localhost:8000 (Android emulator: 10.0.2.2)
  ///
  /// Build vaqtida override qilish uchun:
  ///   flutter run --dart-define=API_BASE_URL=http://IP:8000
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );

  static const String apiVersion = 'v1';

  static String get apiUrl => '$apiBaseUrl/api/$apiVersion';

  /// Ilova versiyasi (backend'ga version-check uchun yuboriladi).
  static const String appVersion = '1.0.0';

  /// Platform (backend'ga yuboriladi).
  static const String iosPlatform = 'IOS';
  static const String androidPlatform = 'ANDROID';

  /// Default til.
  static const String defaultLanguage = 'uz';
  static const List<String> supportedLanguages = ['uz', 'ru', 'en'];

  /// HTTP timeout'lari (millisekund).
  static const int connectTimeout = 15000;
  static const int receiveTimeout = 15000;
}
