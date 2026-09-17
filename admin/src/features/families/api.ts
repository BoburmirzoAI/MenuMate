import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';
import type { FamilyMember, FamilyProfile } from '@/types/domain';

export interface FamilyListItem extends FamilyProfile {
  owner_email: string;
}

export interface FamilyDetail extends FamilyListItem {
  members: FamilyMember[];
}

/** Yangi oila yaratish uchun payload. */
export interface FamilyCreatePayload {
  user_id: number;
  family_name: string;
  city: string;
}

export interface FamilyUpdatePayload {
  id: number;
  family_name?: string;
  city?: string;
}

/** A'zo yaratish/tahrirlash payload. */
export interface FamilyMemberPayload {
  name: string;
  age: number;
  gender: 'MALE' | 'FEMALE';
  health_condition_ids?: number[];
  allergen_ingredient_ids?: number[];
}

export function useFamilies(search?: string) {
  return useQuery({
    queryKey: ['admin', 'families', search ?? ''],
    queryFn: () =>
      api.get<FamilyListItem[]>(endpoints.admin.families.list, {
        params: search ? { search } : undefined,
      }),
  });
}

export function useFamilyDetail(id: number | null) {
  return useQuery({
    queryKey: ['admin', 'families', id],
    enabled: id !== null,
    queryFn: () => api.get<FamilyDetail>(endpoints.admin.families.detail(id!)),
  });
}

export function useCreateFamily() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: FamilyCreatePayload) =>
      api.post<FamilyDetail>(endpoints.admin.families.list, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'families'] }),
  });
}

export function useUpdateFamily() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }: FamilyUpdatePayload) =>
      api.patch<FamilyDetail>(endpoints.admin.families.detail(id), payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'families'] }),
  });
}

export function useDeleteFamily() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(endpoints.admin.families.detail(id)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'families'] }),
  });
}

export function useAddFamilyMember(familyId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: FamilyMemberPayload) =>
      api.post<FamilyMember>(
        `${endpoints.admin.families.detail(familyId)}members/`,
        payload,
      ),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'families'] }),
  });
}

export function useUpdateFamilyMember(familyId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ memberId, ...payload }: FamilyMemberPayload & { memberId: number }) =>
      api.patch<FamilyMember>(
        `${endpoints.admin.families.detail(familyId)}members/${memberId}/`,
        payload,
      ),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'families'] }),
  });
}

export function useDeleteFamilyMember(familyId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (memberId: number) =>
      api.delete(
        `${endpoints.admin.families.detail(familyId)}members/${memberId}/`,
      ),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'families'] }),
  });
}
