import { useQuery } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';
import type { Ingredient, Recipe } from '@/types/domain';

interface RecipesListParams {
  search?: string;
  category?: string;
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
