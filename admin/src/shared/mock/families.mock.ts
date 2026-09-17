import type { FamilyProfile, FamilyMember } from '@/types/domain';

export const mockFamilies: FamilyProfile[] = [
  { id: 1, family_name: 'Sobirjonov oilasi', city: 'Tashkent', member_count: 4, created_at: '2026-01-20T10:00:00Z' },
  { id: 2, family_name: 'Karimov oilasi', city: 'Samarqand', member_count: 5, created_at: '2026-03-25T09:30:00Z' },
  { id: 3, family_name: 'Toshkentli xonadoni', city: 'Bukhoro', member_count: 3, created_at: '2026-05-12T14:20:00Z' },
  { id: 4, family_name: 'Yusupova xonadoni', city: 'Tashkent', member_count: 2, created_at: '2026-06-03T11:00:00Z' },
  { id: 5, family_name: 'Rakhmatov oilasi', city: 'Samarqand', member_count: 6, created_at: '2026-07-20T15:00:00Z' },
];

export const mockFamilyMembers: Record<number, FamilyMember[]> = {
  1: [
    {
      id: 1, name: 'Boburmirzo', age: 27, gender: 'MALE', avatar_emoji: '👨',
      liked_recipes: [1, 5], disliked_recipes: [],
      health_conditions: [], allergen_ingredients: [],
    },
    {
      id: 2, name: 'Aziza', age: 25, gender: 'FEMALE', avatar_emoji: '👩',
      liked_recipes: [2, 8], disliked_recipes: [3],
      health_conditions: [{ id: 1, name: 'Sut allergiyasi', category: 'ALLERGY', icon: '🥛' }],
      allergen_ingredients: [1, 2],
    },
    {
      id: 3, name: 'Ali', age: 5, gender: 'MALE', avatar_emoji: '👦',
      liked_recipes: [4], disliked_recipes: [],
      health_conditions: [], allergen_ingredients: [],
    },
  ],
  2: [
    {
      id: 4, name: 'Karim ota', age: 55, gender: 'MALE', avatar_emoji: '👨',
      liked_recipes: [1], disliked_recipes: [],
      health_conditions: [{ id: 2, name: 'Diabet II', category: 'DIABETES', icon: '💉' }],
      allergen_ingredients: [],
    },
  ],
};
