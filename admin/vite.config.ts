import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

/**
 * Vite konfiguratsiyasi.
 *
 * — Path alias'lar `tsconfig.app.json` bilan sinxron.
 * — Dev-server `/api/*` so'rovlarni Menu Mate Django backend'ga (localhost:8000)
 *   proksi qiladi — brauzerdagi CORS muammosi bo'lmaydi.
 */
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@shared': path.resolve(__dirname, 'src/shared'),
      '@features': path.resolve(__dirname, 'src/features'),
      '@styles': path.resolve(__dirname, 'src/styles'),
      '@router': path.resolve(__dirname, 'src/router'),
      '@types': path.resolve(__dirname, 'src/types'),
    },
  },
  server: {
    port: 5173,
    strictPort: false,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
