import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';

export interface RoleAdmin {
  id: number;
  name: string;
  codename: string;
  description: string;
  permission_ids: number[];
  user_count: number;
  is_active: boolean;
}

export interface PermissionAdmin {
  id: number;
  name: string;
  codename: string;
  description: string;
  parent: number | null;
  role_count: number;
}

export interface EndpointAdmin {
  id: number;
  path: string;
  method: 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';
  name: string;
  description: string;
  access_type: 'public' | 'authenticated' | 'permission';
  required_permission: string | null;
  is_active: boolean;
}

export function useRoles() {
  return useQuery({
    queryKey: ['admin', 'roles'],
    queryFn: () => api.get<RoleAdmin[]>(endpoints.admin.roles.list),
  });
}

export function useUpdateRole() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }: { id: number; permission_ids: number[] }) =>
      api.patch<RoleAdmin>(endpoints.admin.roles.detail(id), payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'roles'] }),
  });
}

export function usePermissions() {
  return useQuery({
    queryKey: ['admin', 'permissions'],
    queryFn: () => api.get<PermissionAdmin[]>(endpoints.admin.permissions),
  });
}

export function useEndpoints() {
  return useQuery({
    queryKey: ['admin', 'endpoints'],
    queryFn: () => api.get<EndpointAdmin[]>(endpoints.admin.endpoints),
  });
}
