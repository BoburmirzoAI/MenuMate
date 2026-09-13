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
    items: [
      { label: 'Boshqaruv paneli', path: '/', icon: LayoutDashboard },
    ],
  },
  {
    label: 'Foydalanuvchilar',
    items: [
      { label: 'Foydalanuvchilar', path: '/users', icon: Users, disabled: true },
      { label: 'Oilalar', path: '/families', icon: UsersRound, disabled: true },
    ],
  },
  {
    label: 'Kontent',
    items: [
      { label: 'Retseptlar', path: '/recipes', icon: ChefHat, disabled: true },
      { label: 'Ingredientlar', path: '/ingredients', icon: Sprout, disabled: true },
      { label: 'Menyular', path: '/menus', icon: CalendarDays, disabled: true },
      { label: 'Xarid ro‘yxatlari', path: '/shopping', icon: ShoppingBasket, disabled: true },
    ],
  },
  {
    label: 'Bildirishnomalar',
    items: [
      { label: 'Bayramlar', path: '/holidays', icon: PartyPopper, disabled: true },
      { label: 'Xabarlar', path: '/notifications', icon: Bell, disabled: true },
    ],
  },
  {
    label: 'Tizim',
    items: [
      { label: 'Ob-havo cache', path: '/weather', icon: Cloud, disabled: true },
      { label: 'Qurilmalar', path: '/devices', icon: Smartphone, disabled: true },
      { label: 'Rollar va ruxsatlar', path: '/permissions', icon: Shield, disabled: true },
    ],
  },
];
