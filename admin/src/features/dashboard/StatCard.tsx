import type { ReactNode } from 'react';
import type { LucideIcon } from 'lucide-react';
import { ArrowUpRight } from 'lucide-react';

import { Card } from '@shared/ui';

import styles from './StatCard.module.css';

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  /** O'zgarish foizi — musbat/manfiy holatga qarab rangi o'zgaradi. */
  delta?: number;
  /** Statistika ostidagi qo'shimcha kontekst (masalan "bu oyda +5"). */
  hint?: ReactNode;
  /** Bosilganda chaqiriladigan funksiya — bo'lsa karta hoverable bo'ladi. */
  onClick?: () => void;
}

/**
 * `<StatCard>` — dashboard'ning KPI kartochkasi.
 *
 * `onClick` berilsa — karta clickable bo'ladi, hover'da arrow ko'rinadi.
 *
 * ```tsx
 * <StatCard label="Foydalanuvchilar" value={128} icon={Users} onClick={...} />
 * ```
 */
export function StatCard({
  label,
  value,
  icon: Icon,
  delta,
  hint,
  onClick,
}: StatCardProps): JSX.Element {
  const deltaTone =
    delta === undefined ? undefined : delta >= 0 ? styles.deltaUp : styles.deltaDown;

  const isClickable = onClick !== undefined;

  return (
    <Card
      hoverable={isClickable}
      onClick={onClick}
      className={isClickable ? styles.clickable : ''}
    >
      <div className={styles.head}>
        <div className={styles.icon}>
          <Icon size={18} />
        </div>
        {delta !== undefined ? (
          <span className={`${styles.delta} ${deltaTone ?? ''}`}>
            {delta >= 0 ? '+' : ''}
            {delta}%
          </span>
        ) : isClickable ? (
          <ArrowUpRight size={16} className={styles.arrow} />
        ) : null}
      </div>
      <div className={styles.label}>{label}</div>
      <div className={styles.value}>{value}</div>
      {hint && <div className={styles.hint}>{hint}</div>}
    </Card>
  );
}
