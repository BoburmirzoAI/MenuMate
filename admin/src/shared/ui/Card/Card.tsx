import type { HTMLAttributes, ReactNode } from 'react';
import clsx from 'clsx';

import styles from './Card.module.css';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /** `hoverable` — sichqoncha tegilganda border/shadow o'zgaradi (list item'lar uchun). */
  hoverable?: boolean;
  /** `padded=false` — ichki padding'ni o'zi berish uchun bekor qilish. */
  padded?: boolean;
  children: ReactNode;
}

/**
 * `<Card>` — asosiy panel/karta konteyneri.
 *
 * Sub-komponentlar bilan tarkibiy struktura:
 * ```tsx
 * <Card>
 *   <CardHeader title="Foydalanuvchilar" action={<Button>+</Button>} />
 *   <CardBody>...</CardBody>
 *   <CardFooter>...</CardFooter>
 * </Card>
 * ```
 */
export function Card({
  hoverable = false,
  padded = true,
  className,
  children,
  ...rest
}: CardProps): JSX.Element {
  return (
    <div
      className={clsx(
        styles.root,
        padded && styles.padded,
        hoverable && styles.hoverable,
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

interface CardHeaderProps {
  title: ReactNode;
  subtitle?: ReactNode;
  action?: ReactNode;
}

/** Karta yuqori qismi — sarlavha va o'ng tomonda amal (Button va h.k.). */
export function CardHeader({ title, subtitle, action }: CardHeaderProps): JSX.Element {
  return (
    <div className={styles.header}>
      <div className={styles.headerText}>
        <div className={styles.title}>{title}</div>
        {subtitle && <div className={styles.subtitle}>{subtitle}</div>}
      </div>
      {action && <div className={styles.headerAction}>{action}</div>}
    </div>
  );
}

/** Karta asosiy tanasi. */
export function CardBody({ children, className }: { children: ReactNode; className?: string }): JSX.Element {
  return <div className={clsx(styles.body, className)}>{children}</div>;
}

/** Karta pastki qismi (odatda amal tugmalari). */
export function CardFooter({ children, className }: { children: ReactNode; className?: string }): JSX.Element {
  return <div className={clsx(styles.footer, className)}>{children}</div>;
}
