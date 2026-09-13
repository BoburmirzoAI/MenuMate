import axios, {
  AxiosError,
  type AxiosInstance,
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
} from 'axios';

import { ApiError, type ApiFailure, type ApiSuccess } from './types';

/**
 * ═══════════════════════════════════════════════════════════════════════════
 *  HTTP klient — Menu Mate backend bilan bogʼlanish qatlami
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * — JWT token'lar `localStorage`da saqlanadi (`storage.ts` orqali).
 * — Har request'ga `Authorization: Bearer <access>` header avtomatik qoʼshiladi.
 * — 401 kelganda `refresh` bilan yangi access olinib, so'rov qayta yuboriladi.
 *   Bir vaqtning oʼzida bir necha 401 bo'lsa, ular navbatga qoʼyilib, bitta
 *   refresh natijasidan foydalanadi (race condition oldini olish).
 * — Backend `{success, id, message, data|errors}` javob qaytaradi. Bu qatlam
 *   javobdan `data` chiqarib bergancha, xatoni esa `ApiError`ga oʼraydi.
 */

const STORAGE_ACCESS = 'menumate_admin_access';
const STORAGE_REFRESH = 'menumate_admin_refresh';

const baseURL = import.meta.env['VITE_API_BASE_URL'] ?? '/api/v1';

/** Token'larni brauzerda saqlash (localStorage — dev qulaylik uchun). */
export const tokenStorage = {
  getAccess: (): string | null => localStorage.getItem(STORAGE_ACCESS),
  getRefresh: (): string | null => localStorage.getItem(STORAGE_REFRESH),
  set: (access: string, refresh: string): void => {
    localStorage.setItem(STORAGE_ACCESS, access);
    localStorage.setItem(STORAGE_REFRESH, refresh);
  },
  clear: (): void => {
    localStorage.removeItem(STORAGE_ACCESS);
    localStorage.removeItem(STORAGE_REFRESH);
  },
};

/**
 * `authClient` — token bilan ishlaydigan axios instance.
 * `rawClient` — refresh so'rovi uchun (interceptor'siz — cheksiz loop bo'lmasin).
 */
export const rawClient: AxiosInstance = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json', 'Accept-Language': 'uz' },
});

export const authClient: AxiosInstance = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json', 'Accept-Language': 'uz' },
});

/* ─────────────────────────  Request interceptor  ─────────────────────────── */

authClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = tokenStorage.getAccess();
  if (token) {
    config.headers.set('Authorization', `Bearer ${token}`);
  }
  return config;
});

/* ─────────────────────────  Response interceptor  ────────────────────────── */

/** Yangi access olish uchun bir vaqtda faqat bitta refresh — qolganlari kutadi. */
let refreshPromise: Promise<string | null> | null = null;

/** `logout` chaqirilishi kerak bo'lganda tashqi handler'ni chaqirish. */
type LogoutHandler = () => void;
let onUnauthorizedHandler: LogoutHandler | null = null;

/** Auth store yaratilgach `client.onUnauthorized(() => authStore.logout())` chaqiradi. */
export function onUnauthorized(handler: LogoutHandler): void {
  onUnauthorizedHandler = handler;
}

/** Refresh — muvaffaqiyatli bo'lsa yangi access qaytaradi, aks holda `null`. */
async function refreshAccessToken(): Promise<string | null> {
  const refresh = tokenStorage.getRefresh();
  if (!refresh) return null;

  try {
    const { data } = await rawClient.post<ApiSuccess<{ access: string; refresh?: string }>>(
      '/users/refresh/',
      { refresh },
    );
    const newAccess = data.data.access;
    const newRefresh = data.data.refresh ?? refresh;
    tokenStorage.set(newAccess, newRefresh);
    return newAccess;
  } catch {
    tokenStorage.clear();
    return null;
  }
}

authClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiFailure>) => {
    const original = error.config as (InternalAxiosRequestConfig & { _retry?: boolean }) | undefined;

    // 1. 401 — refresh bilan qayta urinish (bir marta)
    if (error.response?.status === 401 && original && !original._retry) {
      original._retry = true;
      refreshPromise ??= refreshAccessToken();
      const newAccess = await refreshPromise;
      refreshPromise = null;

      if (newAccess) {
        original.headers.set('Authorization', `Bearer ${newAccess}`);
        return authClient(original);
      }
      onUnauthorizedHandler?.();
    }

    return Promise.reject(toApiError(error));
  },
);

/** AxiosError'ni `ApiError`ga oʼrash. */
function toApiError(error: AxiosError<ApiFailure>): ApiError {
  if (!error.response) return ApiError.network();

  const body = error.response.data;
  if (body && typeof body === 'object' && 'id' in body && 'message' in body) {
    return new ApiError({
      id: body.id,
      message: body.message,
      status: error.response.status,
      ...(body.errors ? { fieldErrors: body.errors } : {}),
    });
  }
  return ApiError.unknown(error.response.status);
}

/* ─────────────────────────  Ergonomik wrapperlar  ────────────────────────── */

/**
 * `api.get('/recipes/')` — `data` maydonini bevosita qaytaradi.
 * Backend'ning `{success, message, data: {...}}` shakli mahalliylashtiriladi.
 */
export const api = {
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await authClient.get<ApiSuccess<T>>(url, config);
    return response.data.data;
  },
  async post<T>(url: string, body?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response = await authClient.post<ApiSuccess<T>>(url, body, config);
    return response.data.data;
  },
  async patch<T>(url: string, body?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response = await authClient.patch<ApiSuccess<T>>(url, body, config);
    return response.data.data;
  },
  async put<T>(url: string, body?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response = await authClient.put<ApiSuccess<T>>(url, body, config);
    return response.data.data;
  },
  async delete<T = void>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await authClient.delete<ApiSuccess<T>>(url, config);
    return response.data.data;
  },
};
