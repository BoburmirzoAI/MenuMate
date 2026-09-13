import { useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { bindAuthToApi, useAuthStore } from '@shared/auth/store';
import { router } from '@router/routes';

/**
 * ═══════════════════════════════════════════════════════════════════════════
 *  App root — global provider'lar va bootstrap
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * — `QueryClient` (TanStack Query) — server-state cache va invalidation.
 * — `RouterProvider` — React Router.
 * — Mount vaqtida `useAuthStore.hydrate()` chaqiriladi — mavjud token bilan
 *   foydalanuvchi profilini qayta oladi.
 * — `bindAuthToApi()` — API 401 kelib refresh imkonsiz bo'lganda store'ni
 *   tozalash uchun bogʼlanish.
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

// `bindAuthToApi` idempotent bo'lgani sabab modul yuklashi vaqtida chaqiramiz.
bindAuthToApi();

export function App(): JSX.Element {
  const hydrate = useAuthStore((state) => state.hydrate);

  useEffect(() => {
    void hydrate();
  }, [hydrate]);

  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}
