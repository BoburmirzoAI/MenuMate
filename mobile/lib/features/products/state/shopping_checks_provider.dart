import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/api/simple_repositories.dart';

/// Xarid ro'yxatidagi tanlangan mahsulotlar holati — real-time yangilanish uchun.
/// Xarid ekrani va Karzinka o'tkazish ekrani orasida bo'lishiladi.
final shoppingLocalChecksProvider =
    NotifierProvider<ShoppingLocalChecksNotifier, Map<int, bool>>(
  ShoppingLocalChecksNotifier.new,
);

class ShoppingLocalChecksNotifier extends Notifier<Map<int, bool>> {
  @override
  Map<int, bool> build() => const {};

  void toggle(int itemId, bool value) {
    state = {...state, itemId: value};
  }

  bool isChecked(ShoppingItem item) => state[item.id] ?? item.isPurchased;
}
