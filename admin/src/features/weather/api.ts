import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';

export interface WeatherSnapshotAdmin {
  id: number;
  city: string;
  temperature: string;
  feels_like: string;
  humidity: number;
  description: string;
  fetched_at: string;
  created_at: string;
}

export function useWeatherSnapshots() {
  return useQuery({
    queryKey: ['admin', 'weather'],
    queryFn: () => api.get<WeatherSnapshotAdmin[]>(endpoints.admin.weather),
  });
}

export function useClearWeatherCache() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => api.delete(endpoints.admin.weather),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'weather'] }),
  });
}
