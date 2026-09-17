import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';
import type { User } from '@/types/domain';

interface UsersListParams {
  search?: string;
  status?: 'active' | 'blocked' | 'unverified';
}

/** Yangi user yaratish uchun payload. */
export interface UserCreatePayload {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone_number?: string;
  birth_date?: string | null;
  gender?: 'MALE' | 'FEMALE' | null;
  timezone?: string;
  language?: 'uz' | 'ru' | 'en';
  is_active?: boolean;
  is_email_verified?: boolean;
  is_push_enabled?: boolean;
  role_ids?: number[];
}

/** User tahrirlash payload — barcha maydonlar ixtiyoriy (patch). */
export interface UserUpdatePayload {
  id: number;
  first_name?: string;
  last_name?: string;
  phone_number?: string;
  birth_date?: string | null;
  gender?: 'MALE' | 'FEMALE' | null;
  timezone?: string;
  language?: 'uz' | 'ru' | 'en';
  is_active?: boolean;
  is_email_verified?: boolean;
  is_push_enabled?: boolean;
  role_ids?: number[];
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

export function useCreateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: UserCreatePayload) =>
      api.post<User>(endpoints.admin.users.list, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['admin', 'users'] });
    },
  });
}

export function useUpdateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }: UserUpdatePayload) =>
      api.patch<User>(endpoints.admin.users.detail(id), payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['admin', 'users'] });
    },
  });
}

export function useSetUserPassword() {
  return useMutation({
    mutationFn: ({ id, password }: { id: number; password: string }) =>
      api.post(`${endpoints.admin.users.detail(id)}set-password/`, { password }),
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
