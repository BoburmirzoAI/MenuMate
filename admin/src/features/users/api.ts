import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';
import type { User } from '@/types/domain';

interface UsersListParams {
  search?: string;
  status?: 'active' | 'blocked' | 'unverified';
}

export function useUsers(params: UsersListParams = {}) {
  return useQuery({
    queryKey: ['admin', 'users', params],
    queryFn: () =>
      api.get<User[]>(endpoints.admin.users.list, {
        params: Object.fromEntries(
          Object.entries(params).filter(([, v]) => v !== undefined && v !== ''),
        ),
      }),
  });
}

export function useUpdateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: { id: number; is_active?: boolean; role_ids?: number[] }) =>
      api.patch<User>(endpoints.admin.users.detail(payload.id), payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['admin', 'users'] });
    },
  });
}

export function useDeleteUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(endpoints.admin.users.detail(id)),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['admin', 'users'] });
    },
  });
}
