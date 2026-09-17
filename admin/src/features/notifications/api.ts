import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';

export interface NotificationAdmin {
  id: number;
  user: number;
  user_email: string;
  kind: string;
  title: string;
  body: string;
  image_url: string;
  is_read: boolean;
  sent_at: string | null;
  created_at: string;
}

export interface BroadcastPayload {
  title: string;
  body: string;
  kind?: string;
  image_url?: string;
}

export function useNotifications() {
  return useQuery({
    queryKey: ['admin', 'notifications'],
    queryFn: () => api.get<NotificationAdmin[]>(endpoints.admin.notifications.list),
  });
}

export function useBroadcastNotification() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: BroadcastPayload) =>
      api.post<{ sent_count: number }>(endpoints.admin.notifications.broadcast, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin', 'notifications'] }),
  });
}
