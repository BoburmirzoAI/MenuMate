import type { Notification } from '@/types/domain';

export const mockNotifications: Notification[] = [
  { id: 1, title: 'Bayram menyusi tayyor', body: 'Mustaqillik kuni uchun maxsus menyu tuzildi', is_read: false, created_at: '2026-09-01T08:00:00Z' },
  { id: 2, title: 'Xarid ro\'yxati yangilandi', body: 'Yangi retseptlar qo\'shildi — 5 ta mahsulot qo\'shildi', is_read: true, created_at: '2026-08-30T14:30:00Z' },
  { id: 3, title: 'Yangi retsept: Osh', body: 'Foydalanuvchilar tavsiya etgan Osh retsepti bazaga qo\'shildi', is_read: true, created_at: '2026-08-25T10:15:00Z' },
  { id: 4, title: 'Ob-havo o\'zgardi', body: 'Bugun issiq — salqin ovqatlar tavsiya qilinadi', is_read: false, created_at: '2026-09-13T06:00:00Z' },
  { id: 5, title: 'Xush kelibsiz!', body: 'Menu Mate ilovasidan foydalanganingiz uchun rahmat', is_read: true, created_at: '2026-01-15T09:35:00Z' },
];
