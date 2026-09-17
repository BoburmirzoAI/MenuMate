import { useQuery } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';

export interface ShoppingItemAdmin {
  id: number;
  ingredient_id: number;
  ingredient_name: string;
  category: string;
  image_url: string;
  total_amount: string;
  unit: string;
  is_purchased: boolean;
}

export interface ShoppingListAdmin {
  id: number;
  menu_id: number;
  family_name: string;
  start_date: string;
  end_date: string;
  total_estimated_cost: string;
  items: ShoppingItemAdmin[];
}

export function useShoppingLists() {
  return useQuery({
    queryKey: ['admin', 'shopping'],
    queryFn: () => api.get<ShoppingListAdmin[]>(endpoints.admin.shopping.list),
  });
}

export function useShoppingByMenu(menuId: number | null) {
  return useQuery({
    queryKey: ['admin', 'shopping', 'by-menu', menuId],
    enabled: menuId !== null,
    queryFn: () => api.get<ShoppingListAdmin>(endpoints.admin.shopping.byMenu(menuId!)),
  });
}
