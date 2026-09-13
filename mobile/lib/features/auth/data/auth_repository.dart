import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/api/api_client.dart';
import '../../../core/storage/secure_storage.dart';
import '../domain/user.dart';

/// Backend auth endpointlariga wrapper.
class AuthRepository {
  AuthRepository({
    required this._client,
    required this._storage,
  });

  final ApiClient _client;
  final SecureStorage _storage;

  /// POST /users/register/
  Future<(User, AuthTokens)> register({
    required String email,
    required String password,
    required String passwordConfirm,
    String? firstName,
    String? lastName,
    String? language,
    String? referralCode,
  }) async {
    final response = await _client.post(
      '/users/register/',
      data: {
        'email': email,
        'password': password,
        'password_confirm': passwordConfirm,
        'first_name': ?firstName,
        'last_name': ?lastName,
        'language': ?language,
        if (referralCode != null && referralCode.isNotEmpty)
          'referral_code': referralCode,
      },
    );
    return _parseAuthResponse(response);
  }

  /// POST /users/login/
  Future<(User, AuthTokens)> login({
    required String email,
    required String password,
  }) async {
    final response = await _client.post(
      '/users/login/',
      data: {'email': email, 'password': password},
    );
    return _parseAuthResponse(response);
  }

  /// POST /users/me/delete/ — hisobni butunlay o'chirish (soft delete)
  Future<void> deleteAccount({required String password}) async {
    await _client.post('/users/me/delete/', data: {
      'password': password,
      'confirmation': 'DELETE',
    });
    await _storage.clear();
  }

  /// POST /users/logout/
  Future<void> logout() async {
    final refresh = await _storage.getRefreshToken();
    if (refresh != null) {
      try {
        await _client.post('/users/logout/', data: {'refresh': refresh});
      } catch (_) {
        // Xato bo'lsa ham davom etamiz — barcha lokal tokenni tozalaymiz
      }
    }
    await _storage.clear();
  }

  /// GET /users/me/
  Future<User> me() async {
    final response = await _client.get('/users/me/');
    return User.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// PATCH /users/me/
  Future<User> updateMe(Map<String, dynamic> fields) async {
    final response = await _client.patch('/users/me/', data: fields);
    return User.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// POST /users/me/change-password/
  Future<void> changePassword({
    required String oldPassword,
    required String newPassword,
    required String newPasswordConfirm,
  }) async {
    await _client.post(
      '/users/me/change-password/',
      data: {
        'old_password': oldPassword,
        'new_password': newPassword,
        'new_password_confirm': newPasswordConfirm,
      },
    );
  }

  /// POST /users/forgot-password/
  Future<void> forgotPassword(String email) async {
    await _client.post('/users/forgot-password/', data: {'email': email});
  }

  /// POST /users/reset-password/
  Future<void> resetPassword({
    required String email,
    required String code,
    required String newPassword,
    required String newPasswordConfirm,
  }) async {
    await _client.post('/users/reset-password/', data: {
      'email': email,
      'code': code,
      'new_password': newPassword,
      'new_password_confirm': newPasswordConfirm,
    });
  }

  /// POST /users/verify-email/send/
  Future<void> sendEmailVerification() async {
    await _client.post('/users/verify-email/send/');
  }

  /// POST /users/verify-email/confirm/
  Future<void> confirmEmailVerification(String code) async {
    await _client.post(
      '/users/verify-email/confirm/',
      data: {'code': code},
    );
  }

  Future<(User, AuthTokens)> _parseAuthResponse(
    Map<String, dynamic> response,
  ) async {
    final data = response['data'] as Map<String, dynamic>;
    final user = User.fromJson(data['user'] as Map<String, dynamic>);
    final tokens = AuthTokens.fromJson(data['tokens'] as Map<String, dynamic>);
    await _storage.saveTokens(access: tokens.access, refresh: tokens.refresh);
    await _storage.saveUserId(user.id);
    return (user, tokens);
  }
}

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository(
    client: ref.watch(apiClientProvider),
    storage: ref.watch(secureStorageProvider),
  );
});
