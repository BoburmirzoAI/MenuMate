import type { ReactNode } from 'react';

import styles from './EmptyState.module.css';

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
}

/**
 * `<EmptyState>` — ro'yxat bo'sh yoki filter bilan hech narsa topilmagan holat.
 *
 * ```tsx
 * <EmptyState icon={<Users />} title="Foydalanuvchi yo'q" action={<Button>+</Button>} />
 * ```
 */
export function EmptyState({ icon, title, description, action }: EmptyStateProps): JSX.Element {
  return (
    <div className={styles.root}>
      {icon && <div className={styles.icon}>{icon}</div>}
      <div className={styles.title}>{title}</div>
      {description && <div className={styles.description}>{description}</div>}
      {action && <div className={styles.action}>{action}</div>}
    </div>
  );
}
