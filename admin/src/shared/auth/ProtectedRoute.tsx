import { Navigate, Outlet, useLocation } from 'react-router-dom';

import { useAuthStore } from './store';

/**
 * `<ProtectedRoute>` — auth talab qiladigan route'lar uchun wrapper.
 *
 * — Foydalanuvchi kirmagan bo'lsa `/login`ga qaytariladi va `from` state bilan
 *   birga uzatiladi — login'dan keyin o'sha sahifaga qaytish uchun.
 * — `authenticating` holatida hech nima ko'rsatmaslik — hydrate tugashini kutish.
 */
export function ProtectedRoute(): JSX.Element {
  const status = useAuthStore((state) => state.status);
  const location = useLocation();

  if (status === 'authenticating') {
    return <div />;
  }

  if (status !== 'authenticated') {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <Outlet />;
}
