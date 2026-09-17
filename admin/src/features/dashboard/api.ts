import { useQuery } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';

export interface DashboardKpi {
  total_users: number;
  active_users: number;
  total_families: number;
  total_recipes: number;
  total_ingredients: number;
  active_menus: number;
  total_menus: number;
  menus_last_30_days: number;
  total_holidays: number;
  total_notifications: number;
  unread_notifications: number;
  total_devices: number;
  devices_with_fcm: number;
}

export interface DashboardStats {
  kpi: DashboardKpi;
  chart_menus_last_30_days: Array<{ day: string; menus: number }>;
}

export function useDashboardStats() {
  return useQuery({
    queryKey: ['admin', 'stats'],
    queryFn: () => api.get<DashboardStats>(endpoints.admin.stats),
  });
}
