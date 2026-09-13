import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

import { api, onUnauthorized, tokenStorage } from '@shared/api/client';
import { endpoints } from '@shared/api/endpoints';
import type { LoginResponse, User } from '@/types/domain';

/**
 * ═══════════════════════════════════════════════════════════════════════════
 *  Auth store — kim kirgan, tokenlar borligi, login/logout amallari.
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * — `user` va `status` `zustand.persist` bilan localStorage'da saqlanadi.
 *   Sahifa yangilansa foydalanuvchi qayta login qilishga majbur emas.
 * — Token'lar `tokenStorage` (api/client.ts) da saqlanadi — bir mustaqil manba.
 * — Login muvaffaqiyatli bo'lsa `access`+`refresh` saqlanadi, `user` state'ga
 *   yoziladi. Interceptor endi har request'ga token qo'shadi.
 */

export type AuthStatus = 'unauthenticated' | 'authenticating' | 'authenticated';

interface AuthState {
  user: User | null;
  status: AuthStatus;
  error: string | null;

  /** Email/parol bilan kirish. */
  login: (email: string, password: string) => Promise<void>;
  /** Serverga xabar berib, token'larni tozalash. */
  logout: () => Promise<void>;
  /** Sahifa yuklanganda `me/` chaqirib profilni yangilash. */
  hydrate: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      status: 'unauthenticated',
      error: null,

      async login(email, password) {
        set({ status: 'authenticating', error: null });
        try {
          const result = await api.post<LoginResponse>(endpoints.auth.login, {
            email,
            password,
          });
          tokenStorage.set(result.tokens.access, result.tokens.refresh);
          set({ user: result.user, status: 'authenticated', error: null });
        } catch (err) {
          set({
            status: 'unauthenticated',
            error: err instanceof Error ? err.message : 'Kirish muvaffaqiyatsiz',
          });
          throw err;
        }
      },

      async logout() {
        try {
          await api.post(endpoints.auth.logout);
        } catch {
          /* backend javob bermasa ham lokal tozalanadi */
        } finally {
          tokenStorage.clear();
          set({ user: null, status: 'unauthenticated', error: null });
        }
      },

      async hydrate() {
        if (!tokenStorage.getAccess()) {
          set({ user: null, status: 'unauthenticated' });
          return;
        }
        try {
          const user = await api.get<User>(endpoints.auth.me);
          set({ user, status: 'authenticated' });
        } catch {
          tokenStorage.clear();
          set({ user: null, status: 'unauthenticated' });
        }
        // `get()` ishlatilmadi — TypeScript unused warning'ga qarshi
        void get;
      },
    }),
    {
      name: 'menumate_admin_auth',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ user: state.user, status: state.status }),
    },
  ),
);

/**
 * API interceptor 401 kelganda va refresh imkonsiz bo'lganda —
 * store'ni tozalasin. Bu bogʼlanish `main.tsx`da bir marta ulanadi.
 */
export function bindAuthToApi(): void {
  onUnauthorized(() => {
    tokenStorage.clear();
    useAuthStore.setState({ user: null, status: 'unauthenticated' });
  });
}
