import { useQuery } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';
import type { FamilyMember, FamilyProfile } from '@/types/domain';

export interface FamilyListItem extends FamilyProfile {
  owner_email: string;
}

export interface FamilyDetail extends FamilyListItem {
  members: FamilyMember[];
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
