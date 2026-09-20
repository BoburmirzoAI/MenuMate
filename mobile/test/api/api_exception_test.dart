import 'package:flutter_test/flutter_test.dart';
import 'package:menu_mate/core/api/api_exception.dart';

void main() {
  group('ApiException.fromResponse', () {
    test('parses standard envelope', () {
      final e = ApiException.fromResponse({
        'success': false,
        'id': 'EMAIL_ALREADY_EXISTS',
        'message': 'Email band',
        'errors': {'field': 'email', 'reason': 'email_already_registered'},
      }, 400);
      expect(e.id, 'EMAIL_ALREADY_EXISTS');
      expect(e.message, 'Email band');
      expect(e.statusCode, 400);
      expect(e.errors, isA<Map>());
      expect((e.errors as Map)['reason'], 'email_already_registered');
    });

    test('defaults when fields missing', () {
      final e = ApiException.fromResponse({}, 500);
      expect(e.id, 'UNKNOWN_ERROR');
      expect(e.message, 'Kutilmagan xatolik');
    });

    test('handles list-form errors (DRF ValidationError)', () {
      final e = ApiException.fromResponse({
        'success': false,
        'id': 'VALIDATION_ERROR',
        'message': 'Noto\'g\'ri',
        'errors': {'password': ['too short']},
      }, 400);
      expect(e.errors, isA<Map>());
      expect((e.errors as Map)['password'], ['too short']);
    });
  });

  group('ApiException.network', () {
    test('returns NETWORK_ERROR id', () {
      final e = ApiException.network();
      expect(e.id, 'NETWORK_ERROR');
      expect(e.statusCode, isNull);
    });
  });

  group('ApiException.unknown', () {
    test('with custom details', () {
      final e = ApiException.unknown('Timeout');
      expect(e.id, 'UNKNOWN_ERROR');
      expect(e.message, 'Timeout');
    });

    test('with no details', () {
      final e = ApiException.unknown();
      expect(e.message, 'Kutilmagan xatolik yuz berdi');
    });
  });

  test('toString shows id and message', () {
    final e = ApiException(id: 'FOO', message: 'bar');
    expect(e.toString(), contains('FOO'));
    expect(e.toString(), contains('bar'));
  });
}
