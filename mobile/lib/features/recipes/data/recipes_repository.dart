import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/api/api_client.dart';
import '../domain/recipe.dart';

class RecipesRepository {
  RecipesRepository(this._client);
  final ApiClient _client;

  /// GET /recipes/ — filter bilan
  Future<({List<Recipe> results, int totalItems, int totalPages, int currentPage})>
      listRecipes({
    String? category,
    String? season,
    bool? isHot,
    String? search,
    List<String>? excludeAllergens,
    int? maxPrepTime,
    int? maxCalories,
    int page = 1,
  }) async {
    final params = <String, dynamic>{'page': page};
    if (category != null) params['category'] = category;
    if (season != null) params['season'] = season;
    if (isHot != null) params['is_hot'] = isHot.toString();
    if (search != null && search.isNotEmpty) params['search'] = search;
    if (excludeAllergens != null && excludeAllergens.isNotEmpty) {
      params['exclude_allergens'] = excludeAllergens.join(',');
    }
    if (maxPrepTime != null) params['max_prep_time'] = maxPrepTime;
    if (maxCalories != null) params['max_calories'] = maxCalories;

    final response = await _client.get('/recipes/', queryParameters: params);
    final data = response['data'] as Map<String, dynamic>;
    final resultsList = data['results'] as List;
    final pagination = data['pagination'] as Map<String, dynamic>;

    return (
      results: resultsList
          .map((e) => Recipe.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalItems: (pagination['total_items'] as int?) ?? 0,
      totalPages: (pagination['total_pages'] as int?) ?? 0,
      currentPage: (pagination['current_page'] as int?) ?? 1,
    );
  }

  /// GET /recipes/{id}/ — to'liq detail
  Future<Recipe> getRecipe(int id) async {
    final response = await _client.get('/recipes/$id/');
    return Recipe.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// GET /recipes/allergens/
  Future<List<AllergenTag>> listAllergens() async {
    final response = await _client.get('/recipes/allergens/');
    final list = response['data'] as List;
    return list.map((e) => AllergenTag.fromJson(e as Map<String, dynamic>)).toList();
  }

  /// GET /recipes/ingredients/
  Future<List<Ingredient>> listIngredients({String? category, String? search}) async {
    final params = <String, dynamic>{};
    if (category != null) params['category'] = category;
    if (search != null && search.isNotEmpty) params['search'] = search;

    final response = await _client.get(
      '/recipes/ingredients/',
      queryParameters: params.isEmpty ? null : params,
    );
    final data = response['data'];
    final list = data is Map ? (data['results'] as List) : (data as List);
    return list.map((e) => Ingredient.fromJson(e as Map<String, dynamic>)).toList();
  }
}

final recipesRepositoryProvider = Provider<RecipesRepository>((ref) {
  return RecipesRepository(ref.watch(apiClientProvider));
});

/// Recipe list with filters.
class RecipeFilters {
  const RecipeFilters({
    this.category,
    this.search,
    this.isHot,
  });
  final String? category;
  final String? search;
  final bool? isHot;

  RecipeFilters copyWith({String? category, String? search, bool? isHot, bool clearCategory = false}) {
    return RecipeFilters(
      category: clearCategory ? null : (category ?? this.category),
      search: search ?? this.search,
      isHot: isHot ?? this.isHot,
    );
  }
}

class RecipeFiltersNotifier extends Notifier<RecipeFilters> {
  @override
  RecipeFilters build() => const RecipeFilters();

  void update(RecipeFilters filters) => state = filters;
}

final recipeFiltersProvider =
    NotifierProvider<RecipeFiltersNotifier, RecipeFilters>(
        RecipeFiltersNotifier.new);

final recipesListProvider = FutureProvider.autoDispose((ref) async {
  final filters = ref.watch(recipeFiltersProvider);
  return ref.watch(recipesRepositoryProvider).listRecipes(
        category: filters.category,
        search: filters.search,
        isHot: filters.isHot,
      );
});

final recipeDetailProvider =
    FutureProvider.autoDispose.family<Recipe, int>((ref, id) async {
  return ref.watch(recipesRepositoryProvider).getRecipe(id);
});
