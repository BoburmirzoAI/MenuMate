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

/**
 * React 19 `JSX.Element` global namespace'ini tiklaydi — komponent qaytish
 * turi sifatida yozish uchun. React 19 default'da `React.JSX` ostiga ko'chgan.
 */
import type { JSX as ReactJSX } from 'react';

declare global {
  namespace JSX {
    type Element = ReactJSX.Element;
    type ElementClass = ReactJSX.ElementClass;
    type ElementAttributesProperty = ReactJSX.ElementAttributesProperty;
    type ElementChildrenAttribute = ReactJSX.ElementChildrenAttribute;
    type LibraryManagedAttributes<C, P> = ReactJSX.LibraryManagedAttributes<C, P>;
    type IntrinsicAttributes = ReactJSX.IntrinsicAttributes;
    type IntrinsicClassAttributes<T> = ReactJSX.IntrinsicClassAttributes<T>;
    type IntrinsicElements = ReactJSX.IntrinsicElements;
  }
}
