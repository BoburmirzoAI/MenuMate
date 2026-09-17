export interface MockPermission {
  id: number;
  name: string;
  codename: string;
  category: string;
  /** Nechta rol'ga biriktirilgan. */
  role_count: number;
}

export interface MockRole {
  id: number;
  name: string;
  codename: string;
  user_count: number;
  /** Ushbu rolga biriktirilgan permission ID'lari. */
  permission_ids: number[];
}

export interface MockEndpoint {
  id: number;
  method: 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';
  path: string;
  access_type: 'PUBLIC' | 'AUTH' | 'PERMISSION';
  required_permission: string | null;
}

/** Barcha permissionlar — kategoriya bo'yicha guruhlangan. */
export const mockPermissions: MockPermission[] = [
  // Users
  { id: 1, name: 'Foydalanuvchilarni ko\'rish', codename: 'users.view', category: 'Users', role_count: 2 },
  { id: 2, name: 'Foydalanuvchini yaratish', codename: 'users.create', category: 'Users', role_count: 1 },
  { id: 3, name: 'Foydalanuvchini tahrirlash', codename: 'users.edit', category: 'Users', role_count: 1 },
  { id: 4, name: 'Foydalanuvchini o\'chirish', codename: 'users.delete', category: 'Users', role_count: 1 },
  { id: 5, name: 'Foydalanuvchini bloklash', codename: 'users.ban', category: 'Users', role_count: 2 },

  // Recipes
  { id: 6, name: 'Retseptlarni ko\'rish', codename: 'recipes.view', category: 'Recipes', role_count: 4 },
  { id: 7, name: 'Retsept yaratish', codename: 'recipes.create', category: 'Recipes', role_count: 2 },
  { id: 8, name: 'Retseptni tahrirlash', codename: 'recipes.edit', category: 'Recipes', role_count: 2 },
  { id: 9, name: 'Retseptni o\'chirish', codename: 'recipes.delete', category: 'Recipes', role_count: 1 },

  // Menus
  { id: 10, name: 'Menyularni ko\'rish', codename: 'menus.view', category: 'Menus', role_count: 4 },
  { id: 11, name: 'Menyu yaratish', codename: 'menus.create', category: 'Menus', role_count: 4 },
  { id: 12, name: 'Menyularni boshqarish (admin)', codename: 'menus.admin', category: 'Menus', role_count: 2 },

  // Notifications
  { id: 13, name: 'Xabarlarni ko\'rish', codename: 'notifications.view', category: 'Notifications', role_count: 4 },
  { id: 14, name: 'Broadcast xabar yuborish', codename: 'notifications.broadcast', category: 'Notifications', role_count: 1 },

  // Holidays
  { id: 15, name: 'Bayramlarni tahrirlash', codename: 'holidays.edit', category: 'Holidays', role_count: 2 },

  // System
  { id: 16, name: 'Rollarni boshqarish', codename: 'system.roles', category: 'System', role_count: 1 },
  { id: 17, name: 'Permissionlarni boshqarish', codename: 'system.permissions', category: 'System', role_count: 1 },
  { id: 18, name: 'Endpoint sozlamalarini o\'zgartirish', codename: 'system.endpoints', category: 'System', role_count: 1 },
  { id: 19, name: 'Ob-havo cache tozalash', codename: 'system.weather', category: 'System', role_count: 2 },
  { id: 20, name: 'Statistikani ko\'rish', codename: 'system.stats', category: 'System', role_count: 2 },
];

export const mockRoles: MockRole[] = [
  {
    id: 1, name: 'Admin', codename: 'admin', user_count: 1,
    permission_ids: mockPermissions.map((p) => p.id),  // barchasi
  },
  {
    id: 2, name: 'Moderator', codename: 'moderator', user_count: 2,
    permission_ids: [1, 3, 5, 6, 7, 8, 10, 13, 15, 19, 20],
  },
  {
    id: 3, name: 'User', codename: 'user', user_count: 3,
    permission_ids: [6, 10, 11, 13],
  },
  {
    id: 4, name: 'Premium', codename: 'premium', user_count: 2,
    permission_ids: [6, 7, 10, 11, 13],
  },
];

export const mockEndpoints: MockEndpoint[] = [
  { id: 1, method: 'POST', path: '/api/v1/users/login/', access_type: 'PUBLIC', required_permission: null },
  { id: 2, method: 'POST', path: '/api/v1/users/register/', access_type: 'PUBLIC', required_permission: null },
  { id: 3, method: 'GET', path: '/api/v1/users/me/', access_type: 'AUTH', required_permission: null },
  { id: 4, method: 'PATCH', path: '/api/v1/users/me/', access_type: 'AUTH', required_permission: null },
  { id: 5, method: 'GET', path: '/api/v1/recipes/', access_type: 'AUTH', required_permission: null },
  { id: 6, method: 'GET', path: '/api/v1/recipes/<id>/', access_type: 'AUTH', required_permission: null },
  { id: 7, method: 'POST', path: '/api/v1/menu/', access_type: 'AUTH', required_permission: null },
  { id: 8, method: 'GET', path: '/api/v1/menu/', access_type: 'AUTH', required_permission: null },
  { id: 9, method: 'DELETE', path: '/api/v1/menu/<id>/', access_type: 'AUTH', required_permission: null },
  { id: 10, method: 'GET', path: '/api/v1/weather/', access_type: 'AUTH', required_permission: null },
  { id: 11, method: 'GET', path: '/api/v1/notifications/', access_type: 'AUTH', required_permission: null },
  { id: 12, method: 'GET', path: '/api/v1/family/', access_type: 'AUTH', required_permission: null },
  { id: 13, method: 'POST', path: '/api/v1/admin/users/', access_type: 'PERMISSION', required_permission: 'admin.users.create' },
  { id: 14, method: 'GET', path: '/api/v1/admin/stats/', access_type: 'PERMISSION', required_permission: 'admin.stats.view' },
];
