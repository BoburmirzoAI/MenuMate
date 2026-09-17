import 'dart:async';
import 'dart:io';

import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';

/// ═════════════════════════════════════════════════════════════════════════
///  FcmService — push notification lifecycle boshqarish qatlami
/// ═════════════════════════════════════════════════════════════════════════
///
/// Vazifalari:
///   1. `Firebase.initializeApp()` — ilova boshlanishida bir marta.
///   2. Foydalanuvchidan notification uchun ruxsat so'rash (Android 13+ va iOS).
///   3. FCM token olish, o'zgarganda kuzatish (`onTokenRefresh`).
///   4. Foreground kelgan xabarlarni `flutter_local_notifications` orqali
///      ekranga chiqarish (default Firebase foreground'da ko'rsatmaydi).
///   5. Notification tap → payload'ni [_tapController] ga uzatish. Router shu
///      stream'ni tinglaydi va kerakli sahifaga o'tkazadi.
///
/// Ilova ochilmagan (terminated) holatda bosilgan xabar `getInitialMessage()`
/// bilan tekshiriladi va deep-link keyingi build'da amalga oshadi.
class FcmService {
  FcmService(this._logger);

  final Logger _logger;

  final FirebaseMessaging _messaging = FirebaseMessaging.instance;
  final FlutterLocalNotificationsPlugin _local =
      FlutterLocalNotificationsPlugin();

  /// Notification bosilganida payload shu stream'ga chiqadi.
  /// Router shu stream'ni tinglab, deep-link amalga oshiradi.
  final StreamController<Map<String, dynamic>> _tapController =
      StreamController<Map<String, dynamic>>.broadcast();
  Stream<Map<String, dynamic>> get onNotificationTap => _tapController.stream;

  bool _initialized = false;
  String? _cachedToken;

  /// FCM tokenini snapshot sifatida qaytaradi (`null` — hali yo'q).
  String? get token => _cachedToken;

  /// Bir marta ishga tushirish. Xato bo'lsa ham ilova ishlashda davom etadi.
  Future<void> initialize() async {
    if (_initialized) return;
    _initialized = true;

    try {
      await Firebase.initializeApp();
    } catch (e) {
      _logger.w('Firebase init failed: $e');
      return;
    }

    // 1. Ruxsat so'raymiz (Android 13+ va iOS).
    await _requestPermission();

    // 2. Local notification plugin — foreground push uchun.
    await _setupLocalNotifications();

    // 3. Token olamiz va o'zgarishlarini kuzatamiz.
    try {
      _cachedToken = await _messaging.getToken();
      _logger.d('FCM token: ${_cachedToken?.substring(0, 20)}…');
    } catch (e) {
      _logger.w('FCM getToken failed: $e');
    }

    _messaging.onTokenRefresh.listen((newToken) {
      _cachedToken = newToken;
      _logger.d('FCM token refreshed');
    });

    // 4. Foreground handler
    FirebaseMessaging.onMessage.listen(_onForegroundMessage);

    // 5. Background handler: user tap qilib ilovaga qaytganida
    FirebaseMessaging.onMessageOpenedApp.listen(_onNotificationTap);

    // 6. Terminated → initial message
    final initial = await _messaging.getInitialMessage();
    if (initial != null) _onNotificationTap(initial);
  }

  Future<void> _requestPermission() async {
    if (Platform.isIOS || Platform.isAndroid) {
      final settings = await _messaging.requestPermission(
        alert: true,
        badge: true,
        sound: true,
        provisional: false,
      );
      _logger.d('FCM permission: ${settings.authorizationStatus}');
    }
  }

  Future<void> _setupLocalNotifications() async {
    const androidInit = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosInit = DarwinInitializationSettings(
      requestAlertPermission: false,   // FCM allaqachon so'radi
      requestBadgePermission: false,
      requestSoundPermission: false,
    );
    const init = InitializationSettings(android: androidInit, iOS: iosInit);

    await _local.initialize(
      init,
      onDidReceiveNotificationResponse: (response) {
        final payload = response.payload;
        if (payload == null || payload.isEmpty) return;
        _tapController.add(_decodePayload(payload));
      },
    );

    // Android: notification channel yaratish (Android 8+ shart)
    if (Platform.isAndroid) {
      await _local
          .resolvePlatformSpecificImplementation<
              AndroidFlutterLocalNotificationsPlugin>()
          ?.createNotificationChannel(
        const AndroidNotificationChannel(
          'menumate_default',
          'Menu Mate xabarlari',
          description: 'Menyu, bayram va boshqa bildirishnomalar',
          importance: Importance.high,
        ),
      );
    }
  }

  void _onForegroundMessage(RemoteMessage message) {
    _logger.d('Foreground push: ${message.notification?.title}');

    final notification = message.notification;
    if (notification == null) return;

    final androidDetails = AndroidNotificationDetails(
      'menumate_default',
      'Menu Mate xabarlari',
      channelDescription: 'Menyu, bayram va boshqa bildirishnomalar',
      importance: Importance.high,
      priority: Priority.high,
      icon: '@mipmap/ic_launcher',
    );
    const iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    _local.show(
      notification.hashCode,
      notification.title,
      notification.body,
      NotificationDetails(android: androidDetails, iOS: iosDetails),
      payload: _encodePayload(message.data),
    );
  }

  void _onNotificationTap(RemoteMessage message) {
    _logger.d('Notification tapped: ${message.data}');
    _tapController.add(Map<String, dynamic>.from(message.data));
  }

  String _encodePayload(Map<String, dynamic> data) {
    return data.entries
        .map((e) => '${Uri.encodeComponent(e.key)}=${Uri.encodeComponent(e.value.toString())}')
        .join('&');
  }

  Map<String, dynamic> _decodePayload(String payload) {
    final map = <String, dynamic>{};
    for (final part in payload.split('&')) {
      final idx = part.indexOf('=');
      if (idx < 0) continue;
      final k = Uri.decodeComponent(part.substring(0, idx));
      final v = Uri.decodeComponent(part.substring(idx + 1));
      map[k] = v;
    }
    return map;
  }

  Future<void> dispose() async {
    await _tapController.close();
  }
}

/// Background message handler — top-level function bo'lishi kerak
/// (Flutter isolate cheklovi). `main.dart`da ro'yxatga olinadi.
@pragma('vm:entry-point')
Future<void> firebaseBackgroundHandler(RemoteMessage message) async {
  // Faqat log — background da ekran chiqarmasa ham FCM system UI ko'rsatadi.
  if (kDebugMode) {
    debugPrint('BG push: ${message.notification?.title}');
  }
}

/// Provider — DI orqali FcmService'ga kirish.
final fcmServiceProvider = Provider<FcmService>((ref) {
  throw UnimplementedError(
    'fcmServiceProvider must be overridden in main() with initialized instance',
  );
});
