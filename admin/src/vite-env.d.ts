/// <reference types="vite/client" />

/**
 * Environment variables uchun turlar.
 * `import.meta.env.VITE_*` autocomplete va type-safety.
 */
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_DEFAULT_LANGUAGE: 'uz' | 'ru' | 'en';
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

/** CSS Modules turini avtomatik keyword bilan qabul qilish. */
declare module '*.module.css' {
  const classes: Record<string, string>;
  export default classes;
}
