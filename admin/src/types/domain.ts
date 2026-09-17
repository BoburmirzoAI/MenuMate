/**
 * Backend model'lariga mos TypeScript turlarim.
 *
 * Django `serializer` chiqarayotgan maydonlar bilan bir xil. Yangi endpoint
 * qo'shilsa yoki maydon nomi o'zgarsa, faqat bu fayl yangilanadi.
 */

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  gender: 'MALE' | 'FEMALE' | null;
  avatar: string | null;
  timezone: string;
  is_email_verified: boolean;
  is_active: boolean;
  is_onboarded: boolean;
  is_premium: boolean;
  roles: Role[];
  created_at: string;
}

export interface Role {
  id: number;
  name: string;
  codename: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  user: User;
  tokens: AuthTokens;
}

/* ─── Family ─── */

export interface FamilyProfile {
  id: number;
  family_name: string;
  city: string;
  member_count: number;
  created_at: string;
}

export interface FamilyMember {
  id: number;
  name: string;
  age: number;
  gender: 'MALE' | 'FEMALE';
  avatar_emoji: string;
  liked_recipes: number[];
  disliked_recipes: number[];
  health_conditions: HealthCondition[];
  allergen_ingredients: number[];
}

export interface HealthCondition {
  id: number;
  name: string;
  category: 'ALLERGY' | 'DIABETES' | 'HEART' | 'WEIGHT' | 'OTHER';
  icon: string;
}

/* ─── Recipes ─── */

export type RecipeCategory =
  | 'BREAKFAST'
  | 'LUNCH'
  | 'DINNER'
  | 'SOUP'
  | 'SALAD'
  | 'DRINK'
  | 'BREAD'
  | 'DESSERT';

export type Season = 'SUMMER' | 'WINTER' | 'ANY';

export interface Recipe {
  id: number;
  name: string;
  name_uz: string;
  name_ru: string;
  name_en: string;
  category: RecipeCategory;
  season: Season;
  prep_time_minutes: number;
  calories_per_serving: number;
  servings: number;
  is_hot: boolean;
  image_url: string;
  allergen_tags: AllergenTag[];
}

export interface AllergenTag {
  id: number;
  name: string;
  code: string;
  icon: string;
}

export interface Ingredient {
  id: number;
  name: string;
  name_uz?: string;
  name_ru?: string;
  name_en?: string;
  category: string;
  unit: string;
  image_url: string;
}

/* ─── Menu ─── */

export type MenuDuration = 'WEEKLY' | 'MONTHLY';
export type MenuStatus = 'ACTIVE' | 'COMPLETED';
export type MealType = 'BREAKFAST' | 'LUNCH' | 'DINNER';
export type MealItemCategory =
  | 'MAIN'
  | 'SOUP'
  | 'SALAD'
  | 'DRINK'
  | 'BREAD'
  | 'DESSERT';

export interface Menu {
  id: number;
  family: number;
  start_date: string;
  end_date: string;
  duration: MenuDuration;
  status: MenuStatus;
  notes: string;
  days: MenuDay[];
  created_at: string;
}

export interface MenuDay {
  id: number;
  date: string;
  is_holiday: boolean;
  holiday_name: string;
  meals: MenuMeal[];
}

export interface MenuMeal {
  id: number;
  meal_type: MealType;
  items: MenuMealItem[];
}

export interface MenuMealItem {
  id: number;
  category: MealItemCategory;
  recipe: Recipe;
}

/* ─── Notifications ─── */

export interface Notification {
  id: number;
  title: string;
  body: string;
  is_read: boolean;
  created_at: string;
}

export interface Holiday {
  id: number;
  name: string;
  date: string;
  emoji: string;
  is_official: boolean;
}
