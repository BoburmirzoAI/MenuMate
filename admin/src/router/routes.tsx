import { createBrowserRouter } from 'react-router-dom';

import { ProtectedRoute } from '@shared/auth/ProtectedRoute';
import { PublicRoute } from '@shared/auth/PublicRoute';
import { AppShell } from '@shared/layout/AppShell';

import { LoginPage } from '@features/auth/LoginPage';
import { DashboardPage } from '@features/dashboard/DashboardPage';

import { NotFoundPage } from './NotFoundPage';
import { paths } from './paths';

/**
 * Ilovaning route ma'lumotlari.
 *
 * Struktura:
 * - `/login`   — Public (kirmagan foydalanuvchi)
 * - `/*`       — Protected (AppShell + Outlet)
 * - `/`        — Dashboard
 * - qolganlari — kelajakda qo'shiladi (Users, Recipes, ...)
 */
export const router = createBrowserRouter([
  {
    element: <PublicRoute />,
    children: [
      { path: paths.login, element: <LoginPage /> },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppShell />,
        children: [
          { path: paths.dashboard, element: <DashboardPage /> },
          // Kelajakdagi sahifalar:
          // { path: paths.users, element: <UsersPage /> },
          // { path: paths.recipes, element: <RecipesPage /> },
        ],
      },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
]);
