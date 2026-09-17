import { create } from 'zustand';

/** Bildirishnoma tone'i (rangi). */
export type ToastTone = 'success' | 'error' | 'info' | 'warning';

export interface Toast {
  id: number;
  tone: ToastTone;
  title: string;
  description?: string;
}

interface ToastState {
  items: Toast[];
  push: (toast: Omit<Toast, 'id'>) => void;
  dismiss: (id: number) => void;
}

let counter = 0;

/**
 * Ilova bo'yicha global toast tizimi.
 *
 * Ishlatish:
 * ```tsx
 * toast.success('Saqlandi', "Foydalanuvchi yaratildi");
 * toast.error('Xato', apiError.message);
 * ```
 */
export const useToastStore = create<ToastState>((set) => ({
  items: [],
  push: (payload) => {
    const id = ++counter;
    set((state) => ({ items: [...state.items, { id, ...payload }] }));
    // Avtomatik yo'qotish — 4 sekund
    window.setTimeout(() => {
      set((state) => ({ items: state.items.filter((t) => t.id !== id) }));
    }, 4000);
  },
  dismiss: (id) =>
    set((state) => ({ items: state.items.filter((t) => t.id !== id) })),
}));

/** Ergonomik facade — komponentga import qilib chaqiriladi. */
export const toast = {
  success: (title: string, description?: string) =>
    useToastStore.getState().push(
      description !== undefined
        ? { tone: 'success', title, description }
        : { tone: 'success', title },
    ),
  error: (title: string, description?: string) =>
    useToastStore.getState().push(
      description !== undefined
        ? { tone: 'error', title, description }
        : { tone: 'error', title },
    ),
  info: (title: string, description?: string) =>
    useToastStore.getState().push(
      description !== undefined
        ? { tone: 'info', title, description }
        : { tone: 'info', title },
    ),
  warning: (title: string, description?: string) =>
    useToastStore.getState().push(
      description !== undefined
        ? { tone: 'warning', title, description }
        : { tone: 'warning', title },
    ),
};
