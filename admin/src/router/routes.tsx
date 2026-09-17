import { createBrowserRouter } from 'react-router-dom';

import { ProtectedRoute } from '@shared/auth/ProtectedRoute';
import { PublicRoute } from '@shared/auth/PublicRoute';
import { AppShell } from '@shared/layout/AppShell';

import { LoginPage } from '@features/auth/LoginPage';
import { DashboardPage } from '@features/dashboard/DashboardPage';
import { UsersPage } from '@features/users/UsersPage';
import { FamiliesPage } from '@features/families/FamiliesPage';
import { RecipesPage } from '@features/recipes/RecipesPage';
import { IngredientsPage } from '@features/ingredients/IngredientsPage';
import { MenusPage } from '@features/menus/MenusPage';
import { ShoppingPage } from '@features/shopping/ShoppingPage';
import { HolidaysPage } from '@features/holidays/HolidaysPage';
import { NotificationsPage } from '@features/notifications/NotificationsPage';
import { WeatherPage } from '@features/weather/WeatherPage';
import { DevicesPage } from '@features/devices/DevicesPage';
import { PermissionsPage } from '@features/permissions/PermissionsPage';

import { NotFoundPage } from './NotFoundPage';
import { paths } from './paths';

/**
 * Ilovaning route jadvali. Barcha admin sahifalar `ProtectedRoute` bilan
 * o'ralgan; `/login` faqat kirmagan foydalanuvchilarga ochiq.
 */
export const router = createBrowserRouter([
  {
    element: <PublicRoute />,
    children: [{ path: paths.login, element: <LoginPage /> }],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppShell />,
        children: [
          { path: paths.dashboard, element: <DashboardPage /> },
          { path: paths.users, element: <UsersPage /> },
          { path: paths.families, element: <FamiliesPage /> },
          { path: paths.recipes, element: <RecipesPage /> },
          { path: paths.ingredients, element: <IngredientsPage /> },
          { path: paths.menus, element: <MenusPage /> },
          { path: paths.shopping, element: <ShoppingPage /> },
          { path: paths.holidays, element: <HolidaysPage /> },
          { path: paths.notifications, element: <NotificationsPage /> },
          { path: paths.weather, element: <WeatherPage /> },
          { path: paths.devices, element: <DevicesPage /> },
          { path: paths.permissions, element: <PermissionsPage /> },
        ],
      },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
]);
