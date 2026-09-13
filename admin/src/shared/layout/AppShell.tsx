import { Outlet } from 'react-router-dom';
import { useState } from 'react';

import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';

import styles from './AppShell.module.css';

/**
 * `<AppShell>` — auth qilingan yuklamalar uchun asosiy qobiq.
 *
 *   ┌────────┬──────────────────────────────────────┐
 *   │        │  Topbar                              │
 *   │Sidebar ├──────────────────────────────────────┤
 *   │        │                                       │
 *   │        │  <Outlet /> — sahifa mazmuni          │
 *   │        │                                       │
 *   └────────┴──────────────────────────────────────┘
 *
 * Sidebar collapsable (kichik ekranlarda ham). Har sahifa `<PageHeader>` bilan
 * boshlab, o'z scroll-container'ini oladi.
 */
export function AppShell(): JSX.Element {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className={styles.root}>
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((v) => !v)} />
      <div className={styles.main}>
        <Topbar />
        <main className={styles.content}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
