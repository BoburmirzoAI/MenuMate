/**
 * Backend endpoint yollari — bir joyda saqlanadi.
 *
 * Har feature'da `import { endpoints } from '@shared/api/endpoints'` bilan
 * ishlatiladi. URL'ni o'zgartirish kerak bo'lsa faqat bu fayl tahrir qilinadi.
 */

export const endpoints = {
  auth: {
    login: '/users/login/',
    logout: '/users/logout/',
    refresh: '/users/refresh/',
    me: '/users/me/',
  },
  // ══ Admin panel API'lari — /api/v1/admin/* ══
  admin: {
    stats: '/admin/stats/',
    users: {
      list: '/admin/users/',
      detail: (id: number | string) => `/admin/users/${id}/`,
    },
    families: {
      list: '/admin/families/',
      detail: (id: number | string) => `/admin/families/${id}/`,
    },
    recipes: {
      list: '/admin/recipes/',
      detail: (id: number | string) => `/admin/recipes/${id}/`,
      ingredients: '/admin/recipes/ingredients/',
      allergens: '/admin/recipes/allergens/',
    },
    menus: {
      list: '/admin/menus/',
      detail: (id: number | string) => `/admin/menus/${id}/`,
    },
    shopping: {
      list: '/admin/shopping/',
      byMenu: (menuId: number | string) => `/admin/shopping/by-menu/${menuId}/`,
    },
    holidays: {
      list: '/admin/notifications/holidays/',
      detail: (id: number | string) => `/admin/notifications/holidays/${id}/`,
    },
    notifications: {
      list: '/admin/notifications/',
      broadcast: '/admin/notifications/broadcast/',
    },
    devices: '/admin/devices/',
    weather: '/admin/weather/',
    roles: {
      list: '/admin/permissions/roles/',
      detail: (id: number | string) => `/admin/permissions/roles/${id}/`,
    },
    permissions: '/admin/permissions/permissions/',
    endpoints: '/admin/permissions/endpoints/',
  },
} as const;
