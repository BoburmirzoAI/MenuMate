/// Backend'dan kelgan xatolikni to'g'ri Dart obyektiga aylantiradi.
///
/// Backend response formati:
///   {
///     "success": false,
///     "id": "EMAIL_ALREADY_EXISTS",
///     "message": "Bu email allaqachon ro'yxatdan o'tgan",
///     "errors": {...}
///   }
class ApiException implements Exception {
  ApiException({
    required this.id,
    required this.message,
    this.errors,
    this.statusCode,
  });

  /// Backend'dagi message key (masalan "EMAIL_ALREADY_EXISTS")
  final String id;

  /// Foydalanuvchi ko'radigan tarjima qilingan matn.
  final String message;

  /// Validation errors (field bo'yicha).
  final dynamic errors;

  /// HTTP status code.
  final int? statusCode;

  factory ApiException.fromResponse(Map<String, dynamic> data, int? code) {
    return ApiException(
      id: data['id']?.toString() ?? 'UNKNOWN_ERROR',
      message: data['message']?.toString() ?? 'Kutilmagan xatolik',
      errors: data['errors'],
      statusCode: code,
    );
  }

  factory ApiException.network() {
    return ApiException(
      id: 'NETWORK_ERROR',
      message: 'Internet ulanishi yo\'q yoki server javob bermayapti',
    );
  }

  factory ApiException.unknown([String? details]) {
    return ApiException(
      id: 'UNKNOWN_ERROR',
      message: details ?? 'Kutilmagan xatolik yuz berdi',
    );
  }

  @override
  String toString() => 'ApiException($id: $message)';
}
