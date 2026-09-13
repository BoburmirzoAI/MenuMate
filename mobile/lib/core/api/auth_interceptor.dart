import 'package:dio/dio.dart';
import 'package:logger/logger.dart';

import '../config/app_config.dart';
import '../storage/secure_storage.dart';

/// Har request'ga `Authorization: Bearer <token>` qo'shadi.
/// 401 xato kelgach refresh token bilan yangi access oladi va so'rovni takrorlaydi.
class AuthInterceptor extends QueuedInterceptor {
  AuthInterceptor(this._storage, this._logger);

  final SecureStorage _storage;
  final Logger _logger;

  bool _isRefreshing = false;

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Login/register/refresh so'rovlarga token qo'shmaymiz.
    final path = options.path;
    final isPublic = path.contains('/users/register/') ||
        path.contains('/users/login/') ||
        path.contains('/users/refresh/') ||
        path.contains('/users/forgot-password/') ||
        path.contains('/users/reset-password/') ||
        path.contains('/devices/version-check/');

    if (!isPublic) {
      final token = await _storage.getAccessToken();
      if (token != null) {
        options.headers['Authorization'] = 'Bearer $token';
      }
    }

    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    // Faqat 401 va login/register bo'lmagan bo'lsa refresh urinamiz.
    final path = err.requestOptions.path;
    final isRefreshPath = path.contains('/users/refresh/');

    if (err.response?.statusCode != 401 || isRefreshPath || _isRefreshing) {
      return handler.next(err);
    }

    _isRefreshing = true;

    try {
      final refresh = await _storage.getRefreshToken();
      if (refresh == null) {
        _isRefreshing = false;
        return handler.next(err);
      }

      final dio = Dio(BaseOptions(baseUrl: AppConfig.apiUrl));
      final response = await dio.post(
        '/users/refresh/',
        data: {'refresh': refresh},
      );

      final newAccess = response.data['access'] as String?;
      if (newAccess == null) {
        _isRefreshing = false;
        await _storage.clear();
        return handler.next(err);
      }

      await _storage.saveTokens(access: newAccess, refresh: refresh);
      _logger.i('Access token muvaffaqiyatli yangilandi');

      // Original so'rovni takrorlaymiz
      err.requestOptions.headers['Authorization'] = 'Bearer $newAccess';
      final retryDio = Dio(BaseOptions(baseUrl: AppConfig.apiUrl));
      final retryResponse = await retryDio.fetch(err.requestOptions);
      _isRefreshing = false;
      return handler.resolve(retryResponse);
    } catch (e) {
      _logger.w('Token yangilash muvaffaqiyatsiz: $e');
      await _storage.clear();
      _isRefreshing = false;
      return handler.next(err);
    }
  }
}
