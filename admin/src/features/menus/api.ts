import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';

export interface MenuAdmin {
  id: number;
  family: number;
  family_name: string;
  owner_email: string;
  start_date: string;
  end_date: string;
  duration: 'WEEKLY' | 'MONTHLY';
  status: 'ACTIVE' | 'COMPLETED';
  notes: string;
  created_at: string;
}

export function useMenus(status?: 'ACTIVE' | 'COMPLETED') {
  return useQuery({
    queryKey: ['admin', 'menus', status ?? 'all'],
    queryFn: () =>
      api.get<MenuAdmin[]>(endpoints.admin.menus.list, {
        params: status ? { status } : undefined,
      }),
  });
}

export function useDeleteMenu() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(endpoints.admin.menus.detail(id)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'menus'] }),
  });
}
