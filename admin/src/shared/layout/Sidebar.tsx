import { NavLink } from 'react-router-dom';
import { ChevronsLeft, ChevronsRight, UtensilsCrossed } from 'lucide-react';
import clsx from 'clsx';

import { navGroups } from './navItems';

import styles from './Sidebar.module.css';

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

/**
 * `<Sidebar>` — chap navigatsiya paneli.
 *
 * — `collapsed=true` bo'lsa faqat ikonlar ko'rinadi (72px kenglik).
 * — `NavLink`ning `.active` klassi joriy sahifani ajratadi.
 * — `disabled` navItem'lar hozircha faol emas (kelajakda qo'shiladigan sahifalar).
 */
export function Sidebar({ collapsed, onToggle }: SidebarProps): JSX.Element {
  return (
    <aside className={clsx(styles.root, collapsed && styles.collapsed)}>
      <div className={styles.brand}>
        <div className={styles.brandIcon}>
          <UtensilsCrossed size={20} />
        </div>
        {!collapsed && (
          <div className={styles.brandText}>
            <div className={styles.brandName}>Menu Mate</div>
            <div className={styles.brandRole}>Admin</div>
          </div>
        )}
      </div>

      <nav className={styles.nav}>
        {navGroups.map((group) => (
          <div key={group.label} className={styles.group}>
            {!collapsed && <div className={styles.groupLabel}>{group.label}</div>}
            {group.items.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  end={item.path === '/'}
                  className={({ isActive }) =>
                    clsx(
                      styles.item,
                      isActive && styles.itemActive,
                      item.disabled && styles.itemDisabled,
                    )
                  }
                  onClick={(e) => {
                    if (item.disabled) e.preventDefault();
                  }}
                  aria-disabled={item.disabled}
                  title={collapsed ? item.label : undefined}
                >
                  <Icon size={18} className={styles.itemIcon} />
                  {!collapsed && <span className={styles.itemLabel}>{item.label}</span>}
                </NavLink>
              );
            })}
          </div>
        ))}
      </nav>

      <button className={styles.collapseBtn} onClick={onToggle} aria-label="Sidebar'ni yig'ish">
        {collapsed ? <ChevronsRight size={16} /> : <ChevronsLeft size={16} />}
        {!collapsed && <span>Yig&#8216;ish</span>}
      </button>
    </aside>
  );
}
