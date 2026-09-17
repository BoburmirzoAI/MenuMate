import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';

export interface HolidayAdmin {
  id: number;
  name: string;
  name_uz?: string;
  name_ru?: string;
  name_en?: string;
  month: number;
  day: number;
  is_movable: boolean;
  description: string;
}

export interface HolidayInput {
  name: string;
  month: number;
  day: number;
  is_movable?: boolean;
  description?: string;
}

export function useHolidays() {
  return useQuery({
    queryKey: ['admin', 'holidays'],
    queryFn: () => api.get<HolidayAdmin[]>(endpoints.admin.holidays.list),
  });
}

export function useCreateHoliday() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: HolidayInput) =>
      api.post<HolidayAdmin>(endpoints.admin.holidays.list, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'holidays'] }),
  });
}

export function useUpdateHoliday() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }: HolidayInput & { id: number }) =>
      api.patch<HolidayAdmin>(endpoints.admin.holidays.detail(id), payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'holidays'] }),
  });
}

export function useDeleteHoliday() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(endpoints.admin.holidays.detail(id)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'holidays'] }),
  });
}
