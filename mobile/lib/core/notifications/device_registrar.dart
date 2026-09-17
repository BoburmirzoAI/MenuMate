import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';

import '../api/api_client.dart';
import '../storage/preferences.dart';
import 'fcm_service.dart';

/// ═════════════════════════════════════════════════════════════════════════
///  DeviceRegistrar — FCM tokenni backendga bog'lash
/// ═════════════════════════════════════════════════════════════════════════
///
/// - Foydalanuvchi login qilganda va token refresh bo'lganda backendga
///   `POST /devices/register/` yuboradi.
/// - Qurilma identifikatorini birinchi marta yaratib (UUID v4)
///   `SharedPreferences`da saqlab qo'yamiz — shu ilova ichida barqaror bo'ladi.
/// - Anonim yoki logout holatlarda ish qilmaydi — token yuborish uchun
///   avtorizatsiya kerak.
class DeviceRegistrar {
  DeviceRegistrar({
    required this.dio,
    required this.fcmService,
    required this.prefs,
    required this.logger,
  });

  final Dio dio;
  final FcmService fcmService;
  final SharedPreferences prefs;
  final Logger logger;

  bool _lastRegistrationSucceeded = false;
  String? _lastRegisteredToken;

  static const _deviceIdKey = 'menumate_device_id';

  /// Login qilingandan darrov chaqiring. Xatolik holatida tinch bo'lib qaytadi.
  Future<void> register() async {
    final fcmToken = fcmService.token;
    if (fcmToken == null || fcmToken.isEmpty) {
      logger.d("FCM token hali yo'q — registration o'tkazib yuborildi");
      return;
    }
    if (_lastRegistrationSucceeded && _lastRegisteredToken == fcmToken) {
      return;
    }

    final deviceId = await _getOrCreateDeviceId();
    final deviceType = _deviceType();

    try {
      await dio.post('/devices/register/', data: {
        'device_id': deviceId,
        'device_type': deviceType,
        'fcm_token': fcmToken,
        'app_version': '1.0.0',
      });
      _lastRegistrationSucceeded = true;
      _lastRegisteredToken = fcmToken;
      logger.i('Device registered (fcm token yangilangan)');
    } on DioException catch (e) {
      logger.w('Device registration failed: ${e.message}');
    }
  }

  /// Qurilmaning barqaror identifikatorini olish. Birinchi marta chaqirilsa
  /// UUID v4 yaratiladi va `SharedPreferences`ga yoziladi.
  Future<String> _getOrCreateDeviceId() async {
    final existing = prefs.getString(_deviceIdKey);
    if (existing != null && existing.isNotEmpty) return existing;

    final newId = const Uuid().v4();
    await prefs.setString(_deviceIdKey, newId);
    return newId;
  }

  String _deviceType() {
    if (kIsWeb) return 'WEB';
    if (Platform.isAndroid) return 'ANDROID';
    if (Platform.isIOS) return 'IOS';
    return 'WEB';
  }
}

/// Provider — DeviceRegistrar'ga kirish.
final deviceRegistrarProvider = Provider<DeviceRegistrar>((ref) {
  return DeviceRegistrar(
    dio: ref.watch(dioProvider),
    fcmService: ref.watch(fcmServiceProvider),
    prefs: ref.watch(sharedPreferencesProvider),
    logger: ref.watch(loggerProvider),
  );
});
