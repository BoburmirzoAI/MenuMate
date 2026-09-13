import 'dart:io' show Platform;

import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';

import '../config/app_config.dart';
import '../l10n/language_provider.dart';
import '../storage/secure_storage.dart';
import 'api_exception.dart';
import 'auth_interceptor.dart';

/// Backend'ga so'rovlar yuboradigan API klient (Dio wrapper).
class ApiClient {
  ApiClient({required this._dio, required this._logger});

  final Dio _dio;
  final Logger _logger;

  Dio get dio => _dio;

  Future<Map<String, dynamic>> get(
    String path, {
    Map<String, dynamic>? queryParameters,
  }) async {
    return _handle(() => _dio.get(path, queryParameters: queryParameters));
  }

  Future<Map<String, dynamic>> post(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
  }) async {
    return _handle(() => _dio.post(path, data: data, queryParameters: queryParameters));
  }

  Future<Map<String, dynamic>> patch(String path, {dynamic data}) async {
    return _handle(() => _dio.patch(path, data: data));
  }

  Future<Map<String, dynamic>> put(String path, {dynamic data}) async {
    return _handle(() => _dio.put(path, data: data));
  }

  Future<Map<String, dynamic>> delete(String path, {dynamic data}) async {
    return _handle(() => _dio.delete(path, data: data));
  }

  Future<Map<String, dynamic>> _handle(
    Future<Response> Function() request,
  ) async {
    try {
      final response = await request();
      final data = response.data;
      if (data is Map<String, dynamic>) return data;
      return {'data': data};
    } on DioException catch (e) {
      _logger.w('API xato ${e.requestOptions.uri}: ${e.message}');
      if (e.response?.data is Map<String, dynamic>) {
        throw ApiException.fromResponse(
          e.response!.data as Map<String, dynamic>,
          e.response?.statusCode,
        );
      }
      if (e.type == DioExceptionType.connectionError ||
          e.type == DioExceptionType.connectionTimeout ||
          e.type == DioExceptionType.receiveTimeout) {
        throw ApiException.network();
      }
      throw ApiException.unknown(e.message);
    } catch (e) {
      _logger.e('Kutilmagan xato: $e');
      throw ApiException.unknown(e.toString());
    }
  }
}

// ---------------------------------------------------------------------
// Providers
// ---------------------------------------------------------------------

final loggerProvider = Provider<Logger>((ref) {
  return Logger(
    printer: PrettyPrinter(
      methodCount: 0,
      lineLength: 80,
      colors: true,
      printEmojis: true,
      dateTimeFormat: DateTimeFormat.onlyTimeAndSinceStart,
    ),
    level: kDebugMode ? Level.debug : Level.warning,
  );
});

final dioProvider = Provider<Dio>((ref) {
  final storage = ref.watch(secureStorageProvider);
  final logger = ref.watch(loggerProvider);
  // Til o'zgarsa Dio qayta quriladi — barcha keyingi so'rovlar yangi Accept-Language bilan.
  final lang = ref.watch(languageProvider);

  // Android emulator localhost'ga 10.0.2.2 orqali kiradi
  var baseUrl = AppConfig.apiUrl;
  if (!kIsWeb && Platform.isAndroid) {
    baseUrl = baseUrl.replaceFirst('localhost', '10.0.2.2');
  }

  final dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: Duration(milliseconds: AppConfig.connectTimeout),
      receiveTimeout: Duration(milliseconds: AppConfig.receiveTimeout),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Accept-Language': lang,
      },
      responseType: ResponseType.json,
    ),
  );

  dio.interceptors.add(AuthInterceptor(storage, logger));

  if (kDebugMode) {
    dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
        error: true,
        logPrint: (obj) => logger.d(obj.toString()),
      ),
    );
  }

  return dio;
});

final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient(
    dio: ref.watch(dioProvider),
    logger: ref.watch(loggerProvider),
  );
});
