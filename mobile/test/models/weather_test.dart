import 'package:flutter_test/flutter_test.dart';
import 'package:menu_mate/core/api/simple_repositories.dart';

void main() {
  group('Weather.fromJson', () {
    test('parses valid json with numeric strings', () {
      final w = Weather.fromJson({
        'city': 'Tashkent',
        'temperature': '25.5',
        'feels_like': '27.1',
        'humidity': 60,
        'description': 'clear',
      });
      expect(w.city, 'Tashkent');
      expect(w.temperature, 25.5);
      expect(w.feelsLike, 27.1);
      expect(w.humidity, 60);
    });

    test('parses valid json with double values', () {
      final w = Weather.fromJson({
        'city': 'Samarkand',
        'temperature': 30.0,
        'feels_like': 33.0,
        'humidity': 40,
        'description': 'sunny',
      });
      expect(w.temperature, 30.0);
    });

    test('emoji per temperature range', () {
      Weather w(double t) => Weather(
        city: '', temperature: t, feelsLike: t, humidity: 0, description: '',
      );
      expect(w(35).emoji, '🥵');
      expect(w(27).emoji, '☀️');
      expect(w(20).emoji, '🌤️');
      expect(w(10).emoji, '⛅');
      expect(w(0).emoji, '❄️');
      expect(w(-10).emoji, '🥶');
    });

    test('missing required field throws', () {
      expect(
        () => Weather.fromJson({'temperature': '10'}),
        throwsA(isA<TypeError>()),
      );
    });
  });
}
