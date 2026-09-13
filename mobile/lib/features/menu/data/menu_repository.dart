import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/api/api_client.dart';
import '../domain/menu.dart';

class MenuRepository {
  MenuRepository(this._client);
  final ApiClient _client;

  /// GET /menu/
  Future<List<Menu>> listMenus() async {
    final response = await _client.get('/menu/');
    final data = response['data'];
    final list = data is Map ? (data['results'] as List) : (data as List);
    return list.map((e) => Menu.fromJson(e as Map<String, dynamic>)).toList();
  }

  /// GET /menu/{id}/
  Future<Menu> getMenu(int id) async {
    final response = await _client.get('/menu/$id/');
    return Menu.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// POST /menu/ — bo'sh menyu yaratadi
  Future<Menu> createMenu({
    required DateTime startDate,
    String duration = 'WEEKLY',
  }) async {
    final response = await _client.post('/menu/', data: {
      'start_date': startDate.toIso8601String().split('T').first,
      'duration': duration,
    });
    return Menu.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// DELETE /menu/{id}/
  Future<void> delete(int id) async {
    await _client.delete('/menu/$id/');
  }

  /// POST /menu/{id}/clear/
  Future<Menu> clearMenu(int id) async {
    final response = await _client.post('/menu/$id/clear/');
    return Menu.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// GET /menu/{id}/stats/
  Future<Map<String, dynamic>> getStats(int id) async {
    final response = await _client.get('/menu/$id/stats/');
    return response['data'] as Map<String, dynamic>;
  }

  /// GET /menu/meals/{mealId}/recommendations/?category=X
  Future<List<RecipeShort>> getRecommendations({
    required int mealId,
    required String category,
  }) async {
    final response = await _client.get(
      '/menu/meals/$mealId/recommendations/',
      queryParameters: {'category': category},
    );
    final list = response['data'] as List;
    return list.map((e) => RecipeShort.fromJson(e as Map<String, dynamic>)).toList();
  }

  /// POST /menu/meals/{mealId}/items/
  Future<MenuMealItem> addItem({
    required int mealId,
    required String category,
    required int recipeId,
  }) async {
    final response = await _client.post(
      '/menu/meals/$mealId/items/',
      data: {'category': category, 'recipe_id': recipeId},
    );
    return MenuMealItem.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// DELETE /menu/meals/{mealId}/items/{itemId}/
  Future<void> removeItem({required int mealId, required int itemId}) async {
    await _client.delete('/menu/meals/$mealId/items/$itemId/');
  }
}

final menuRepositoryProvider = Provider<MenuRepository>((ref) {
  return MenuRepository(ref.watch(apiClientProvider));
});

/// Foydalanuvchining oxirgi menyusi (bor bo'lsa).
final currentMenuProvider = FutureProvider<Menu?>((ref) async {
  final repo = ref.watch(menuRepositoryProvider);
  final list = await repo.listMenus();
  if (list.isEmpty) return null;
  return repo.getMenu(list.first.id);
});
