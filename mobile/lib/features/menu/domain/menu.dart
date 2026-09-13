import 'package:equatable/equatable.dart';

class RecipeShort extends Equatable {
  const RecipeShort({
    required this.id,
    required this.name,
    required this.category,
    required this.prepTimeMinutes,
    required this.caloriesPerServing,
    required this.isHot,
    this.imageUrl = '',
  });

  final int id;
  final String name;
  final String category;
  final int prepTimeMinutes;
  final int caloriesPerServing;
  final bool isHot;
  final String imageUrl;

  bool get hasImage => imageUrl.isNotEmpty;

  factory RecipeShort.fromJson(Map<String, dynamic> json) => RecipeShort(
        id: json['id'] as int,
        name: json['name'] as String? ?? json['name_uz'] as String? ?? '',
        category: json['category'] as String,
        prepTimeMinutes: json['prep_time_minutes'] as int? ?? 0,
        caloriesPerServing: json['calories_per_serving'] as int? ?? 0,
        isHot: (json['is_hot'] as bool?) ?? true,
        imageUrl: (json['image_url'] as String?) ?? '',
      );

  @override
  List<Object?> get props => [id, name, category];
}

class MenuMealItem extends Equatable {
  const MenuMealItem({
    required this.id,
    required this.category,
    required this.recipe,
  });

  final int id;
  final String category; // MAIN/SOUP/SALAD/DRINK/BREAD/DESSERT
  final RecipeShort recipe;

  factory MenuMealItem.fromJson(Map<String, dynamic> json) => MenuMealItem(
        id: json['id'] as int,
        category: json['category'] as String,
        recipe: RecipeShort.fromJson(json['recipe'] as Map<String, dynamic>),
      );

  @override
  List<Object?> get props => [id, category, recipe];
}

class MenuMeal extends Equatable {
  const MenuMeal({
    required this.id,
    required this.mealType,
    required this.items,
  });

  final int id;
  final String mealType; // BREAKFAST/LUNCH/DINNER
  final List<MenuMealItem> items;

  factory MenuMeal.fromJson(Map<String, dynamic> json) {
    final items = (json['items'] as List?)
            ?.map((e) => MenuMealItem.fromJson(e as Map<String, dynamic>))
            .toList() ??
        [];
    return MenuMeal(
      id: json['id'] as int,
      mealType: json['meal_type'] as String,
      items: items,
    );
  }

  MenuMealItem? itemFor(String category) =>
      items.where((it) => it.category == category).firstOrNull;

  RecipeShort? get mainRecipe {
    final main = itemFor('MAIN');
    return main?.recipe ?? (items.isNotEmpty ? items.first.recipe : null);
  }

  @override
  List<Object?> get props => [id, mealType, items];
}

class MenuDay extends Equatable {
  const MenuDay({
    required this.id,
    required this.date,
    required this.meals,
    this.isHoliday = false,
    this.holidayName = '',
  });

  final int id;
  final DateTime date;
  final List<MenuMeal> meals;
  final bool isHoliday;
  final String holidayName;

  factory MenuDay.fromJson(Map<String, dynamic> json) {
    final meals = (json['meals'] as List)
        .map((e) => MenuMeal.fromJson(e as Map<String, dynamic>))
        .toList();
    return MenuDay(
      id: json['id'] as int,
      date: DateTime.parse(json['date'] as String),
      meals: meals,
      isHoliday: (json['is_holiday'] as bool?) ?? false,
      holidayName: (json['holiday_name'] as String?) ?? '',
    );
  }

  MenuMeal? mealFor(String type) => meals.where((m) => m.mealType == type).firstOrNull;

  @override
  List<Object?> get props => [id, date, meals];
}

class Menu extends Equatable {
  const Menu({
    required this.id,
    required this.startDate,
    required this.endDate,
    required this.duration,
    required this.status,
    required this.days,
    this.notes = '',
  });

  final int id;
  final DateTime startDate;
  final DateTime endDate;
  final String duration; // WEEKLY/MONTHLY
  final String status;   // ACTIVE/COMPLETED
  final List<MenuDay> days;
  final String notes;

  factory Menu.fromJson(Map<String, dynamic> json) {
    final days = (json['days'] as List?)
            ?.map((e) => MenuDay.fromJson(e as Map<String, dynamic>))
            .toList() ??
        [];
    return Menu(
      id: json['id'] as int,
      startDate: DateTime.parse(json['start_date'] as String),
      endDate: DateTime.parse(json['end_date'] as String),
      duration: (json['duration'] as String?) ?? 'WEEKLY',
      status: (json['status'] as String?) ?? 'ACTIVE',
      days: days,
      notes: (json['notes'] as String?) ?? '',
    );
  }

  int get totalMeals => days.fold(0, (n, d) => n + d.meals.length);
  int get totalItems =>
      days.fold(0, (n, d) => n + d.meals.fold(0, (m, meal) => m + meal.items.length));

  MenuDay? get today {
    final now = DateTime.now();
    return days.where((d) =>
        d.date.year == now.year && d.date.month == now.month && d.date.day == now.day).firstOrNull;
  }

  @override
  List<Object?> get props => [id, startDate, endDate, days];
}
