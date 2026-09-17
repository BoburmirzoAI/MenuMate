import { useQuery } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';

export interface DeviceAdmin {
  id: number;
  user: number;
  user_email: string;
  device_id: string;
  device_type: 'ANDROID' | 'IOS' | 'WEB';
  app_version: string;
  is_active: boolean;
  fcm_token_set: boolean;
  last_login: string;
  created_at: string;
}

interface DevicesParams {
  search?: string;
  device_type?: 'ANDROID' | 'IOS' | 'WEB';
}

export function useDevices(params: DevicesParams = {}) {
  return useQuery({
    queryKey: ['admin', 'devices', params],
    queryFn: () =>
      api.get<DeviceAdmin[]>(endpoints.admin.devices, {
        params: Object.fromEntries(
          Object.entries(params).filter(([, v]) => v !== undefined && v !== '' && v !== 'all'),
        ),
      }),
  });
}
