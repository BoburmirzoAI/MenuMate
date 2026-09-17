import {
  LayoutDashboard,
  Users,
  UsersRound,
  ChefHat,
  Sprout,
  CalendarDays,
  ShoppingBasket,
  Bell,
  PartyPopper,
  Cloud,
  Smartphone,
  Shield,
  type LucideIcon,
} from 'lucide-react';

/**
 * Sidebar navigatsiya konfiguratsiyasi.
 *
 * Bir joyda saqlanadi — sahifa qo'shsangiz shu ro'yxatga bir qator qo'shib qo'yasiz,
 * tayyor route va Sidebar avtomatik yangilanadi.
 */
export interface NavItem {
  label: string;
  path: string;
  icon: LucideIcon;
  /** Vaqtincha o'chirilgan (ishlab chiqilmoqda) — Sidebar'da xira ko'rinadi. */
  disabled?: boolean;
}

export interface NavGroup {
  label: string;
  items: NavItem[];
}

export const navGroups: NavGroup[] = [
  {
    label: 'Umumiy',
    items: [{ label: 'Boshqaruv paneli', path: '/', icon: LayoutDashboard }],
  },
  {
    label: 'Foydalanuvchilar',
    items: [
      { label: 'Foydalanuvchilar', path: '/users', icon: Users },
      { label: 'Oilalar', path: '/families', icon: UsersRound },
    ],
  },
  {
    label: 'Kontent',
    items: [
      { label: 'Retseptlar', path: '/recipes', icon: ChefHat },
      { label: 'Ingredientlar', path: '/ingredients', icon: Sprout },
      { label: 'Menyular', path: '/menus', icon: CalendarDays },
      { label: 'Xarid roʼyxatlari', path: '/shopping', icon: ShoppingBasket },
    ],
  },
  {
    label: 'Bildirishnomalar',
    items: [
      { label: 'Bayramlar', path: '/holidays', icon: PartyPopper },
      { label: 'Xabarlar', path: '/notifications', icon: Bell },
    ],
  },
  {
    label: 'Tizim',
    items: [
      { label: 'Ob-havo cache', path: '/weather', icon: Cloud },
      { label: 'Qurilmalar', path: '/devices', icon: Smartphone },
      { label: 'Rollar va ruxsatlar', path: '/permissions', icon: Shield },
    ],
  },
];
