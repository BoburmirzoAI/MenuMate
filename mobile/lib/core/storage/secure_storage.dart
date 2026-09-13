import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// JWT tokenlarni xavfsiz saqlash (iOS Keychain / Android EncryptedSharedPrefs).
class SecureStorage {
  SecureStorage(this._storage);

  final FlutterSecureStorage _storage;

  static const _kAccessToken = 'access_token';
  static const _kRefreshToken = 'refresh_token';
  static const _kUserId = 'user_id';

  Future<void> saveTokens({
    required String access,
    required String refresh,
  }) async {
    await _storage.write(key: _kAccessToken, value: access);
    await _storage.write(key: _kRefreshToken, value: refresh);
  }

  Future<String?> getAccessToken() => _storage.read(key: _kAccessToken);

  Future<String?> getRefreshToken() => _storage.read(key: _kRefreshToken);

  Future<void> saveUserId(int id) =>
      _storage.write(key: _kUserId, value: id.toString());

  Future<int?> getUserId() async {
    final v = await _storage.read(key: _kUserId);
    return v == null ? null : int.tryParse(v);
  }

  Future<void> clear() async {
    await _storage.deleteAll();
  }
}

final secureStorageProvider = Provider<SecureStorage>((ref) {
  const storage = FlutterSecureStorage(
    iOptions: IOSOptions(accessibility: KeychainAccessibility.unlocked),
  );
  return SecureStorage(storage);
});
