import 'package:flutter_test/flutter_test.dart';
import 'package:menu_mate/core/api/simple_repositories.dart';

Map<String, dynamic> _base({
  int id = 1,
  bool purchased = false,
  bool kgoAvailable = true,
}) => {
      'id': id,
      'ingredient': {
        'name': 'Olma',
        'category': 'FRUIT',
        'image_url': 'https://x/olma.png',
      },
      'total_amount': '500',
      'unit': 'g',
      'is_purchased': purchased,
      'kgo_available': kgoAvailable,
      'kgo_price_per_unit': '12490',
      'kgo_unit': 'kg',
      'price_total': '6245',
      'kgo_title': 'Olma Jeromin',
      'kgo_image_url': 'https://x/olma-real.png',
      'kgo_product_url': 'https://korzinka.uz/product/olma',
      'kgo_weight': '1kg',
    };

void main() {
  group('ShoppingItem.fromJson', () {
    test('parses valid item', () {
      final item = ShoppingItem.fromJson(_base());
      expect(item.id, 1);
      expect(item.ingredientName, 'Olma');
      expect(item.ingredientCategory, 'FRUIT');
      expect(item.totalAmount, '500');
      expect(item.kgoAvailable, isTrue);
      expect(item.kgoTitle, 'Olma Jeromin');
    });

    test('defaults are applied when fields missing', () {
      final j = _base();
      j.remove('is_purchased');
      j.remove('kgo_available');
      j.remove('kgo_unit');
      final item = ShoppingItem.fromJson(j);
      expect(item.isPurchased, isFalse);
      expect(item.kgoAvailable, isTrue);
      expect(item.kgoUnit, '');
    });

    test('null string fields fall back to empty string', () {
      final j = _base();
      j['kgo_title'] = null;
      j['kgo_image_url'] = null;
      final item = ShoppingItem.fromJson(j);
      expect(item.kgoTitle, '');
      expect(item.kgoImageUrl, '');
    });

    test('copyWith flips purchased', () {
      final item = ShoppingItem.fromJson(_base(purchased: false));
      final flipped = item.copyWith(isPurchased: true);
      expect(item.isPurchased, isFalse);
      expect(flipped.isPurchased, isTrue);
      expect(flipped.id, item.id);
    });

    test('equatable compares id and purchased', () {
      final a = ShoppingItem.fromJson(_base(id: 1, purchased: false));
      final b = ShoppingItem.fromJson(_base(id: 1, purchased: false));
      final c = ShoppingItem.fromJson(_base(id: 1, purchased: true));
      expect(a, equals(b));
      expect(a, isNot(equals(c)));
    });
  });
}
