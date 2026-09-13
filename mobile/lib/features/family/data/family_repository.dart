import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/api/api_client.dart';
import '../domain/family.dart';

class FamilyRepository {
  FamilyRepository(this._client);
  final ApiClient _client;

  /// GET /family/
  Future<FamilyProfile?> getFamily() async {
    try {
      final response = await _client.get('/family/');
      return FamilyProfile.fromJson(response['data'] as Map<String, dynamic>);
    } catch (_) {
      return null;
    }
  }

  /// POST /family/
  Future<FamilyProfile> createFamily({
    required String familyName,
    required String city,
  }) async {
    final response = await _client.post('/family/', data: {
      'family_name': familyName,
      'city': city,
    });
    return FamilyProfile.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// PATCH /family/
  Future<FamilyProfile> updateFamily(Map<String, dynamic> fields) async {
    final response = await _client.patch('/family/', data: fields);
    return FamilyProfile.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// GET /family/members/
  Future<List<FamilyMember>> listMembers() async {
    final response = await _client.get('/family/members/');
    final list = response['data'] as List;
    return list.map((e) => FamilyMember.fromJson(e as Map<String, dynamic>)).toList();
  }

  /// POST /family/members/
  Future<FamilyMember> createMember({
    required String name,
    required int age,
    required String gender,
    List<int> healthConditionIds = const [],
    List<int> allergenIngredientIds = const [],
    List<int> likedRecipeIds = const [],
    List<int> dislikedRecipeIds = const [],
  }) async {
    final response = await _client.post('/family/members/', data: {
      'name': name,
      'age': age,
      'gender': gender,
      if (healthConditionIds.isNotEmpty) 'health_condition_ids': healthConditionIds,
      if (allergenIngredientIds.isNotEmpty) 'allergen_ingredient_ids': allergenIngredientIds,
      if (likedRecipeIds.isNotEmpty) 'liked_recipe_ids': likedRecipeIds,
      if (dislikedRecipeIds.isNotEmpty) 'disliked_recipe_ids': dislikedRecipeIds,
    });
    return FamilyMember.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// PATCH /family/members/{id}/
  Future<FamilyMember> updateMember(int id, Map<String, dynamic> fields) async {
    final response = await _client.patch('/family/members/$id/', data: fields);
    return FamilyMember.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// DELETE /family/members/{id}/
  Future<void> deleteMember(int id) async {
    await _client.delete('/family/members/$id/');
  }

  /// GET /family/health-conditions/?category=
  Future<List<HealthCondition>> listHealthConditions({String? category}) async {
    final response = await _client.get(
      '/family/health-conditions/',
      queryParameters: category != null ? {'category': category} : null,
    );
    final list = response['data'] as List;
    return list.map((e) => HealthCondition.fromJson(e as Map<String, dynamic>)).toList();
  }
}

final familyRepositoryProvider = Provider<FamilyRepository>((ref) {
  return FamilyRepository(ref.watch(apiClientProvider));
});

final myFamilyProvider = FutureProvider<FamilyProfile?>((ref) async {
  return ref.watch(familyRepositoryProvider).getFamily();
});

final familyMembersProvider = FutureProvider<List<FamilyMember>>((ref) async {
  return ref.watch(familyRepositoryProvider).listMembers();
});

final healthConditionsProvider =
    FutureProvider.family<List<HealthCondition>, String?>((ref, category) async {
  return ref.watch(familyRepositoryProvider).listHealthConditions(category: category);
});
