import type { ReactNode } from 'react';
import type { LucideIcon } from 'lucide-react';

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
}

/**
 * `<StatCard>` — dashboard'ning KPI kartochkasi.
 *
 * ```tsx
 * <StatCard label="Foydalanuvchilar" value={128} icon={Users} delta={12} />
 * ```
 */
export function StatCard({ label, value, icon: Icon, delta, hint }: StatCardProps): JSX.Element {
  const deltaTone =
    delta === undefined ? undefined : delta >= 0 ? styles.deltaUp : styles.deltaDown;

  return (
    <Card>
      <div className={styles.head}>
        <div className={styles.icon}>
          <Icon size={18} />
        </div>
        {delta !== undefined && (
          <span className={`${styles.delta} ${deltaTone ?? ''}`}>
            {delta >= 0 ? '+' : ''}
            {delta}%
          </span>
        )}
      </div>
      <div className={styles.label}>{label}</div>
      <div className={styles.value}>{value}</div>
      {hint && <div className={styles.hint}>{hint}</div>}
    </Card>
  );
}
