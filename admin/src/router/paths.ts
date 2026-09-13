/**
 * Route yo'llari — bir joyda, string literal sifatida.
 * Bu — jonli link'lar va `navigate()` chaqiruvlarida `paths.dashboard` bilan
 * yozib, magic-string'lardan qochish uchun.
 */
export const paths = {
  login: '/login',
  dashboard: '/',
  users: '/users',
  families: '/families',
  recipes: '/recipes',
  ingredients: '/ingredients',
  menus: '/menus',
  shopping: '/shopping',
  holidays: '/holidays',
  notifications: '/notifications',
  weather: '/weather',
  devices: '/devices',
  permissions: '/permissions',
} as const;
