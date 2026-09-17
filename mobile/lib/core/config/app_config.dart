/// Ilova sozlamalari — API URL, versiya va h.k.
///
/// Production'da bu qiymatlar `--dart-define` orqali build vaqtida beriladi:
///   flutter run --dart-define=API_BASE_URL=https://api.menumate.uz
class AppConfig {
  AppConfig._();

  /// Backend API base URL.
  ///
  /// - **Production/Release APK** — Cloudflare Tunnel orqali kelayotgan doimiy
  ///   URL: `https://menumate.anipulse.uz`. Task beruvchi telefoni istagan
  ///   tarmoqda bo'lsa ham backend'ga ulanadi (Mac yoqilgan bo'lishi sharti).
  /// - **Lokal dev (Chrome, iOS Simulator, real telefon debug)** — build
  ///   vaqtida override qilib berish:
  ///     flutter run --dart-define=API_BASE_URL=http://localhost:8000
  ///     flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000  (Android emulator)
  ///     flutter run --dart-define=API_BASE_URL=http://192.168.1.110:8000  (LAN)
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://menumate.anipulse.uz',
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
