import type { Menu } from '@/types/domain';

export const mockMenus: Menu[] = [
  {
    id: 1, family: 1, start_date: '2026-09-14', end_date: '2026-09-20',
    duration: 'WEEKLY', status: 'ACTIVE', notes: '',
    created_at: '2026-09-13T08:00:00Z',
    days: [],
  },
  {
    id: 2, family: 2, start_date: '2026-09-01', end_date: '2026-09-30',
    duration: 'MONTHLY', status: 'ACTIVE', notes: 'Bayram menyusi bilan',
    created_at: '2026-08-30T14:00:00Z',
    days: [],
  },
  {
    id: 3, family: 1, start_date: '2026-08-15', end_date: '2026-08-21',
    duration: 'WEEKLY', status: 'COMPLETED', notes: '',
    created_at: '2026-08-14T09:00:00Z',
    days: [],
  },
  {
    id: 4, family: 3, start_date: '2026-09-10', end_date: '2026-09-16',
    duration: 'WEEKLY', status: 'ACTIVE', notes: '',
    created_at: '2026-09-09T11:00:00Z',
    days: [],
  },
  {
    id: 5, family: 5, start_date: '2026-09-01', end_date: '2026-09-30',
    duration: 'MONTHLY', status: 'ACTIVE', notes: '',
    created_at: '2026-08-31T15:00:00Z',
    days: [],
  },
];
