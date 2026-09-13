import 'package:equatable/equatable.dart';

class AllergenTag extends Equatable {
  const AllergenTag({
    required this.id,
    required this.slug,
    required this.name,
  });
  final int id;
  final String slug;
  final String name;

  factory AllergenTag.fromJson(Map<String, dynamic> json) => AllergenTag(
        id: json['id'] as int,
        slug: json['slug'] as String,
        name: (json['name'] as String?) ?? '',
      );

  @override
  List<Object?> get props => [id, slug];
}

class Ingredient extends Equatable {
  const Ingredient({
    required this.id,
    required this.name,
    required this.category,
    required this.defaultUnit,
    this.imageUrl = '',
  });
  final int id;
  final String name;
  final String category;
  final String defaultUnit;
  final String imageUrl;

  bool get hasImage => imageUrl.isNotEmpty;

  factory Ingredient.fromJson(Map<String, dynamic> json) => Ingredient(
        id: json['id'] as int,
        name: (json['name'] as String?) ?? '',
        category: json['category'] as String,
        defaultUnit: json['default_unit'] as String,
        imageUrl: (json['image_url'] as String?) ?? '',
      );

  @override
  List<Object?> get props => [id, name];
}

class RecipeIngredient extends Equatable {
  const RecipeIngredient({
    required this.id,
    required this.ingredient,
    required this.amount,
    required this.unit,
  });
  final int id;
  final Ingredient ingredient;
  final String amount;
  final String unit;

  factory RecipeIngredient.fromJson(Map<String, dynamic> json) => RecipeIngredient(
        id: json['id'] as int,
        ingredient: Ingredient.fromJson(json['ingredient'] as Map<String, dynamic>),
        amount: json['amount'].toString(),
        unit: json['unit'] as String,
      );

  @override
  List<Object?> get props => [id];
}

class RecipeStep extends Equatable {
  const RecipeStep({
    required this.id,
    required this.order,
    required this.description,
  });
  final int id;
  final int order;
  final String description;

  factory RecipeStep.fromJson(Map<String, dynamic> json) => RecipeStep(
        id: json['id'] as int,
        order: json['order'] as int,
        description: (json['description'] as String?) ?? '',
      );

  @override
  List<Object?> get props => [id, order];
}

class Recipe extends Equatable {
  const Recipe({
    required this.id,
    required this.name,
    required this.category,
    required this.season,
    required this.prepTimeMinutes,
    required this.caloriesPerServing,
    required this.servings,
    required this.isHot,
    this.description = '',
    this.imageUrl = '',
    this.allergenTags = const [],
    this.ingredients = const [],
    this.steps = const [],
  });

  final int id;
  final String name;
  final String description;
  final String category;
  final String season;
  final int prepTimeMinutes;
  final int caloriesPerServing;
  final int servings;
  final bool isHot;
  final String imageUrl;
  final List<AllergenTag> allergenTags;
  final List<RecipeIngredient> ingredients;
  final List<RecipeStep> steps;

  bool get hasImage => imageUrl.isNotEmpty;

  factory Recipe.fromJson(Map<String, dynamic> json) {
    final tags = (json['allergen_tags'] as List?)
            ?.map((e) => AllergenTag.fromJson(e as Map<String, dynamic>))
            .toList() ??
        [];
    final ings = (json['ingredients'] as List?)
            ?.map((e) => RecipeIngredient.fromJson(e as Map<String, dynamic>))
            .toList() ??
        [];
    final steps = (json['steps'] as List?)
            ?.map((e) => RecipeStep.fromJson(e as Map<String, dynamic>))
            .toList() ??
        [];
    return Recipe(
      id: json['id'] as int,
      name: (json['name'] as String?) ?? '',
      description: (json['description'] as String?) ?? '',
      category: json['category'] as String,
      season: (json['season'] as String?) ?? 'ALL',
      prepTimeMinutes: (json['prep_time_minutes'] as int?) ?? 0,
      caloriesPerServing: (json['calories_per_serving'] as int?) ?? 0,
      servings: (json['servings'] as int?) ?? 1,
      isHot: (json['is_hot'] as bool?) ?? true,
      imageUrl: (json['image_url'] as String?) ?? '',
      allergenTags: tags,
      ingredients: ings,
      steps: steps,
    );
  }

  @override
  List<Object?> get props => [id, name];
}

/// Recipe kategoriya uchun O'zbekcha label + emoji.
class RecipeCategoryInfo {
  static const map = {
    'BREAKFAST': ('☕', 'Nonushta'),
    'LUNCH': ('🍲', 'Tushlik'),
    'DINNER': ('🍽️', 'Kechki'),
    'SALAD': ('🥗', 'Salat'),
    'SOUP': ('🥣', 'Sho\'rva'),
    'DRINK': ('🥤', 'Ichimlik'),
    'DESSERT': ('🍰', 'Shirinlik'),
    'BREAD': ('🥖', 'Non'),
    'SNACK': ('🍿', 'Yengil'),
  };

  static String emoji(String category) => map[category]?.$1 ?? '🍴';
  static String label(String category) => map[category]?.$2 ?? category;
}
