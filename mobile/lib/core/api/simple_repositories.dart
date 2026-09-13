import 'package:equatable/equatable.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'api_client.dart';


class Weather extends Equatable {
  const Weather({
    required this.city,
    required this.temperature,
    required this.feelsLike,
    required this.humidity,
    required this.description,
  });

  final String city;
  final double temperature;
  final double feelsLike;
  final int humidity;
  final String description;

  factory Weather.fromJson(Map<String, dynamic> json) => Weather(
        city: json['city'] as String,
        temperature: double.parse(json['temperature'].toString()),
        feelsLike: double.parse(json['feels_like'].toString()),
        humidity: json['humidity'] as int,
        description: json['description'] as String,
      );

  String get emoji {
    final t = temperature;
    if (t >= 30) return '🥵';
    if (t >= 25) return '☀️';
    if (t >= 15) return '🌤️';
    if (t >= 5) return '⛅';
    if (t >= -5) return '❄️';
    return '🥶';
  }

  @override
  List<Object?> get props => [city, temperature];
}

final weatherProvider = FutureProvider<Weather?>((ref) async {
  final client = ref.watch(apiClientProvider);
  try {
    final response = await client.get('/weather/');
    return Weather.fromJson(response['data'] as Map<String, dynamic>);
  } catch (_) {
    return null; // Weather kelmasa ilova buzilmaydi
  }
});

class ShoppingItem extends Equatable {
  const ShoppingItem({
    required this.id,
    required this.ingredientName,
    required this.ingredientCategory,
    required this.totalAmount,
    required this.unit,
    this.isPurchased = false,
    this.kgoAvailable = true,
    this.kgoPricePerUnit,
    this.kgoUnit = '',
    this.priceTotal,
    this.ingredientImageUrl = '',
    // Karzinka real API'dan
    this.kgoTitle = '',
    this.kgoImageUrl = '',
    this.kgoProductUrl = '',
    this.kgoWeight = '',
  });

  final int id;
  final String ingredientName;
  final String ingredientCategory;
  final String ingredientImageUrl;
  final String totalAmount;
  final String unit;
  final bool isPurchased;

  // Karzinka Go (real API'dan)
  final bool kgoAvailable;
  final String? kgoPricePerUnit; // so'm/birlik
  final String kgoUnit;
  final String? priceTotal;      // shu qatorning jami narxi (so'm)
  final String kgoTitle;         // Karzinka mahsulot nomi ("Olma Jeromin Oʻzb, kg")
  final String kgoImageUrl;      // Karzinka mahsulot rasmi
  final String kgoProductUrl;    // Deep link Karzinka Go ilovasiga
  final String kgoWeight;        // "1кг", "400 гр"

  factory ShoppingItem.fromJson(Map<String, dynamic> json) {
    final ing = json['ingredient'] as Map<String, dynamic>;
    return ShoppingItem(
      id: json['id'] as int,
      ingredientName: (ing['name'] as String?) ?? '',
      ingredientCategory: ing['category'] as String,
      ingredientImageUrl: (ing['image_url'] as String?) ?? '',
      totalAmount: json['total_amount'].toString(),
      unit: json['unit'] as String,
      isPurchased: (json['is_purchased'] as bool?) ?? false,
      kgoAvailable: (json['kgo_available'] as bool?) ?? true,
      kgoPricePerUnit: json['kgo_price_per_unit']?.toString(),
      kgoUnit: (json['kgo_unit'] as String?) ?? '',
      priceTotal: json['price_total']?.toString(),
      kgoTitle: (json['kgo_title'] as String?) ?? '',
      kgoImageUrl: (json['kgo_image_url'] as String?) ?? '',
      kgoProductUrl: (json['kgo_product_url'] as String?) ?? '',
      kgoWeight: (json['kgo_weight'] as String?) ?? '',
    );
  }

  ShoppingItem copyWith({bool? isPurchased}) => ShoppingItem(
        id: id,
        ingredientName: ingredientName,
        ingredientCategory: ingredientCategory,
        ingredientImageUrl: ingredientImageUrl,
        totalAmount: totalAmount,
        unit: unit,
        isPurchased: isPurchased ?? this.isPurchased,
        kgoAvailable: kgoAvailable,
        kgoPricePerUnit: kgoPricePerUnit,
        kgoUnit: kgoUnit,
        priceTotal: priceTotal,
        kgoTitle: kgoTitle,
        kgoImageUrl: kgoImageUrl,
        kgoProductUrl: kgoProductUrl,
        kgoWeight: kgoWeight,
      );

  @override
  List<Object?> get props => [id, isPurchased];
}

class ShoppingList extends Equatable {
  const ShoppingList({
    required this.id,
    required this.menuId,
    required this.itemsByCategory,
    required this.totalItems,
    this.availableItems = 0,
    this.unavailableItems = const [],
    this.totalEstimatedCost = '0',
  });

  final int id;
  final int menuId;
  final Map<String, List<ShoppingItem>> itemsByCategory;
  final int totalItems;
  final int availableItems;
  final List<ShoppingItem> unavailableItems;
  final String totalEstimatedCost; // so'm

  factory ShoppingList.fromJson(Map<String, dynamic> json) {
    final raw = (json['items_by_category'] as Map<String, dynamic>?) ?? {};
    final map = <String, List<ShoppingItem>>{};
    raw.forEach((k, v) {
      map[k] = (v as List)
          .map((e) => ShoppingItem.fromJson(e as Map<String, dynamic>))
          .toList();
    });
    final unavail = (json['unavailable_items'] as List?)
            ?.map((e) => ShoppingItem.fromJson(e as Map<String, dynamic>))
            .toList() ??
        const [];
    return ShoppingList(
      id: json['id'] as int,
      menuId: json['menu_id'] as int,
      itemsByCategory: map,
      totalItems: json['total_items'] as int,
      availableItems: (json['available_items'] as int?) ?? 0,
      unavailableItems: unavail,
      totalEstimatedCost: json['total_estimated_cost']?.toString() ?? '0',
    );
  }

  int get purchasedCount =>
      itemsByCategory.values.expand((l) => l).where((i) => i.isPurchased).length;

  @override
  List<Object?> get props => [id, menuId, itemsByCategory];
}

class ProductsRepository {
  ProductsRepository(this._client);
  final ApiClient _client;

  Future<ShoppingList> getMenuShoppingList(int menuId) async {
    final response = await _client.get('/menu/$menuId/products/');
    return ShoppingList.fromJson(response['data'] as Map<String, dynamic>);
  }

  Future<ShoppingItem> toggleItem(int itemId, bool purchased) async {
    final response = await _client.patch(
      '/products/shopping-items/$itemId/',
      data: {'is_purchased': purchased},
    );
    return ShoppingItem.fromJson(response['data'] as Map<String, dynamic>);
  }
}

final productsRepositoryProvider = Provider<ProductsRepository>((ref) {
  return ProductsRepository(ref.watch(apiClientProvider));
});

final shoppingListProvider =
    FutureProvider.family<ShoppingList, int>((ref, menuId) async {
  return ref.watch(productsRepositoryProvider).getMenuShoppingList(menuId);
});
