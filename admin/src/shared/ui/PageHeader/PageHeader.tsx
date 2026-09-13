import type { ReactNode } from 'react';

import styles from './PageHeader.module.css';

interface PageHeaderProps {
  title: string;
  description?: string;
  /** O'ng tarafda amal tugmalari. */
  actions?: ReactNode;
}

/**
 * `<PageHeader>` — sahifa yuqorisidagi sarlavha va amal tugmalari uchun bir xil naqsh.
 *
 * ```tsx
 * <PageHeader title="Foydalanuvchilar" description="Barcha ro'yxatdan o'tganlar"
 *             actions={<Button leftIcon={<Plus />}>Yangi</Button>} />
 * ```
 */
export function PageHeader({ title, description, actions }: PageHeaderProps): JSX.Element {
  return (
    <header className={styles.root}>
      <div className={styles.text}>
        <h1 className={styles.title}>{title}</h1>
        {description && <p className={styles.description}>{description}</p>}
      </div>
      {actions && <div className={styles.actions}>{actions}</div>}
    </header>
  );
}
