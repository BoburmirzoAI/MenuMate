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

/* ─── Roles ─── */

export function useRoles() {
  return useQuery({
    queryKey: ['admin', 'roles'],
    queryFn: () => api.get<RoleAdmin[]>(endpoints.admin.roles.list),
  });
}

export interface RoleWritePayload {
  name?: string;
  description?: string;
  is_active?: boolean;
  permission_ids?: number[];
}

export function useCreateRole() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: RoleWritePayload) =>
      api.post<RoleAdmin>(endpoints.admin.roles.list, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'roles'] }),
  });
}

export function useUpdateRole() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }: { id: number } & RoleWritePayload) =>
      api.patch<RoleAdmin>(endpoints.admin.roles.detail(id), payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'roles'] }),
  });
}

export function useDeleteRole() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(endpoints.admin.roles.detail(id)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'roles'] }),
  });
}

/* ─── Permissions ─── */

export function usePermissions() {
  return useQuery({
    queryKey: ['admin', 'permissions'],
    queryFn: () => api.get<PermissionAdmin[]>(endpoints.admin.permissions.list),
  });
}

export interface PermissionWritePayload {
  name?: string;
  codename?: string;
  description?: string;
  parent?: number | null;
}

export function useCreatePermission() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: PermissionWritePayload) =>
      api.post<PermissionAdmin>(endpoints.admin.permissions.list, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'permissions'] }),
  });
}

export function useUpdatePermission() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }: { id: number } & PermissionWritePayload) =>
      api.patch<PermissionAdmin>(endpoints.admin.permissions.detail(id), payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'permissions'] }),
  });
}

export function useDeletePermission() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(endpoints.admin.permissions.detail(id)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'permissions'] }),
  });
}

/* ─── Endpoints (faqat sozlash — path/method boshqarilmaydi) ─── */

export function useEndpoints() {
  return useQuery({
    queryKey: ['admin', 'endpoints'],
    queryFn: () => api.get<EndpointAdmin[]>(endpoints.admin.endpoints.list),
  });
}

export interface EndpointWritePayload {
  access_type?: EndpointAdmin['access_type'];
  permission?: number | null;
  is_active?: boolean;
  name?: string;
  description?: string;
}

export function useUpdateEndpoint() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }: { id: number } & EndpointWritePayload) =>
      api.patch<EndpointAdmin>(endpoints.admin.endpoints.detail(id), payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'endpoints'] }),
  });
}
