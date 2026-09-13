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
  users: {
    list: '/users/',
    detail: (id: number | string) => `/users/${id}/`,
  },
  families: {
    list: '/family/',
    members: '/family/members/',
    memberDetail: (id: number | string) => `/family/members/${id}/`,
    healthConditions: '/family/health-conditions/',
  },
  recipes: {
    list: '/recipes/',
    detail: (id: number | string) => `/recipes/${id}/`,
    allergens: '/recipes/allergens/',
    ingredients: '/recipes/ingredients/',
  },
  menus: {
    list: '/menu/',
    detail: (id: number | string) => `/menu/${id}/`,
    stats: (id: number | string) => `/menu/${id}/stats/`,
    clear: (id: number | string) => `/menu/${id}/clear/`,
  },
  products: {
    shoppingList: (menuId: number | string) => `/menu/${menuId}/products/`,
    item: (itemId: number | string) => `/products/shopping-items/${itemId}/`,
  },
  weather: '/weather/',
  notifications: {
    list: '/notifications/',
    read: (id: number | string) => `/notifications/${id}/read/`,
    markAll: '/notifications/mark-all-read/',
    holidays: '/notifications/holidays/',
    upcoming: '/notifications/holidays/upcoming/',
  },
} as const;
