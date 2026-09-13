import { Navigate, Outlet } from 'react-router-dom';

import { useAuthStore } from './store';

/**
 * `<PublicRoute>` — `/login` kabi sahifalar uchun.
 *
 * Foydalanuvchi allaqachon kirgan bo'lsa dashboard'ga qaytariladi (login sahifasi
 * ochilib turmasin uchun).
 */
export function PublicRoute(): JSX.Element {
  const status = useAuthStore((state) => state.status);

  if (status === 'authenticated') {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
