import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';
import type { AllergenTag, Ingredient, Recipe } from '@/types/domain';

interface RecipesListParams {
  search?: string;
  category?: string;
}

/** Retsept yaratish/tahrirlash payload. */
export interface RecipePayload {
  name_uz: string;
  name_ru: string;
  name_en: string;
  description_uz?: string;
  description_ru?: string;
  description_en?: string;
  category: string;
  season: string;
  prep_time_minutes: number;
  calories_per_serving: number;
  servings: number;
  is_hot: boolean;
  image_url?: string;
  allergen_tag_ids?: number[];
}

/** Ingredient yaratish/tahrirlash payload. */
export interface IngredientPayload {
  name_uz: string;
  name_ru: string;
  name_en: string;
  category: string;
  default_unit: string;
  image_url?: string;
  allergen_tag_ids?: number[];
}

export function useRecipes(params: RecipesListParams = {}) {
  return useQuery({
    queryKey: ['admin', 'recipes', params],
    queryFn: () =>
      api.get<Recipe[]>(endpoints.admin.recipes.list, {
        params: Object.fromEntries(
          Object.entries(params).filter(([, v]) => v !== undefined && v !== '' && v !== 'all'),
        ),
      }),
  });
}

export function useCreateRecipe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: RecipePayload) =>
      api.post<Recipe>(endpoints.admin.recipes.list, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'recipes'] }),
  });
}

export function useUpdateRecipe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }: RecipePayload & { id: number }) =>
      api.patch<Recipe>(endpoints.admin.recipes.detail(id), payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'recipes'] }),
  });
}

export function useDeleteRecipe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(endpoints.admin.recipes.detail(id)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'recipes'] }),
  });
}

export function useIngredients(params: RecipesListParams = {}) {
  return useQuery({
    queryKey: ['admin', 'ingredients', params],
    queryFn: () =>
      api.get<Ingredient[]>(endpoints.admin.recipes.ingredients, {
        params: Object.fromEntries(
          Object.entries(params).filter(([, v]) => v !== undefined && v !== '' && v !== 'all'),
        ),
      }),
  });
}

export function useCreateIngredient() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: IngredientPayload) =>
      api.post<Ingredient>(endpoints.admin.recipes.ingredients, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'ingredients'] }),
  });
}

export function useUpdateIngredient() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }: IngredientPayload & { id: number }) =>
      api.patch<Ingredient>(`${endpoints.admin.recipes.ingredients}${id}/`, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'ingredients'] }),
  });
}

export function useDeleteIngredient() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(`${endpoints.admin.recipes.ingredients}${id}/`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'ingredients'] }),
  });
}

export function useAllergens() {
  return useQuery({
    queryKey: ['admin', 'allergens'],
    queryFn: () => api.get<AllergenTag[]>(endpoints.admin.recipes.allergens),
  });
}
