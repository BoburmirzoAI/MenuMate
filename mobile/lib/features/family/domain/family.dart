import 'package:equatable/equatable.dart';

class FamilyProfile extends Equatable {
  const FamilyProfile({
    required this.id,
    required this.familyName,
    required this.city,
    this.membersCount = 0,
  });

  final int id;
  final String familyName;
  final String city;
  final int membersCount;

  factory FamilyProfile.fromJson(Map<String, dynamic> json) => FamilyProfile(
        id: json['id'] as int,
        familyName: json['family_name'] as String,
        city: json['city'] as String,
        membersCount: (json['members_count'] as int?) ?? 0,
      );

  @override
  List<Object?> get props => [id, familyName, city, membersCount];
}

class HealthCondition extends Equatable {
  const HealthCondition({
    required this.id,
    required this.name,
    required this.category,
    this.description = '',
  });

  final int id;
  final String name;
  final String category; // ALLERGY, DIABETES, HEART, OBESITY, OTHER
  final String description;

  factory HealthCondition.fromJson(Map<String, dynamic> json) => HealthCondition(
        id: json['id'] as int,
        name: json['name'] as String,
        category: json['category'] as String,
        description: (json['description'] as String?) ?? '',
      );

  @override
  List<Object?> get props => [id, name, category];
}

class FamilyMember extends Equatable {
  const FamilyMember({
    required this.id,
    required this.name,
    required this.age,
    required this.gender,
    this.healthConditions = const [],
    this.allergenIngredientIds = const [],
    this.likedRecipeIds = const [],
    this.dislikedRecipeIds = const [],
  });

  final int id;
  final String name;
  final int age;
  final String gender; // MALE/FEMALE/OTHER
  final List<HealthCondition> healthConditions;
  final List<int> allergenIngredientIds;
  final List<int> likedRecipeIds;
  final List<int> dislikedRecipeIds;

  factory FamilyMember.fromJson(Map<String, dynamic> json) {
    final hcs = (json['health_conditions'] as List?)
            ?.map((e) => HealthCondition.fromJson(e as Map<String, dynamic>))
            .toList() ??
        [];
    final allergens = (json['allergen_ingredients'] as List?)
            ?.map((e) => (e as Map)['id'] as int)
            .toList() ??
        [];
    return FamilyMember(
      id: json['id'] as int,
      name: json['name'] as String,
      age: json['age'] as int,
      gender: json['gender'] as String,
      healthConditions: hcs,
      allergenIngredientIds: allergens,
    );
  }

  @override
  List<Object?> get props => [id, name, age, gender, healthConditions];
}
