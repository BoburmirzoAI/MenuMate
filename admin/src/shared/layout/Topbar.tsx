import { useState, useRef, useEffect } from 'react';
import { LogOut, ChevronDown, User as UserIcon } from 'lucide-react';

import { useAuthStore } from '@shared/auth/store';

import styles from './Topbar.module.css';

/**
 * `<Topbar>` — asosiy shell'ning yuqori paneli.
 *
 * — Chapda: joriy sahifa uchun bo'sh joy (breadcrumb kelajakda).
 * — O'ngda: foydalanuvchi menyusi (avatar + ism + chiqish tugmasi).
 */
export function Topbar(): JSX.Element {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Tashqariga bosilganda menyu yopiladi.
  useEffect(() => {
    if (!menuOpen) return;
    const handleClick = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [menuOpen]);

  const displayName = user
    ? `${user.first_name} ${user.last_name}`.trim() || user.email
    : '';
  const initial = displayName.charAt(0).toUpperCase();

  return (
    <header className={styles.root}>
      <div className={styles.spacer} />
      <div className={styles.userMenuContainer} ref={menuRef}>
        <button
          className={styles.userBtn}
          onClick={() => setMenuOpen((v) => !v)}
          aria-haspopup="menu"
          aria-expanded={menuOpen}
        >
          <span className={styles.avatar}>{initial || <UserIcon size={16} />}</span>
          <span className={styles.userText}>
            <span className={styles.userName}>{displayName || 'Foydalanuvchi'}</span>
            {user?.email && <span className={styles.userEmail}>{user.email}</span>}
          </span>
          <ChevronDown size={14} className={styles.chevron} />
        </button>

        {menuOpen && (
          <div className={styles.menu} role="menu">
            <button
              className={styles.menuItem}
              onClick={() => {
                setMenuOpen(false);
                void logout();
              }}
              role="menuitem"
            >
              <LogOut size={16} />
              <span>Chiqish</span>
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
