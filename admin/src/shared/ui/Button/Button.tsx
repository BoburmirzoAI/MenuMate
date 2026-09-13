import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from 'react';
import clsx from 'clsx';

import styles from './Button.module.css';

/** Vizual variant — brand accent, minimal, xatarli va oddiy matn. */
export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';

/** O'lchamlar — dashboard'da faqat 3 ta o'lcham etarli. */
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  /** Yuklanish holatida bosilmaydi va spinner ko'rsatiladi. */
  loading?: boolean;
  /** Tugma to'liq kenglikda cho'ziladi. */
  block?: boolean;
  /** Chap tomonga qo'yiladigan ikon (lucide-react). */
  leftIcon?: ReactNode;
  /** O'ng tomonga qo'yiladigan ikon. */
  rightIcon?: ReactNode;
}

/**
 * `<Button>` — ilova ichida asosiy tugma.
 *
 * ```tsx
 * <Button variant="primary" leftIcon={<Plus size={16} />}>Yangi qo'shish</Button>
 * <Button loading>Yuklanmoqda</Button>
 * <Button variant="danger" size="sm" onClick={handleDelete}>O'chirish</Button>
 * ```
 */
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  {
    variant = 'primary',
    size = 'md',
    loading = false,
    block = false,
    leftIcon,
    rightIcon,
    disabled,
    className,
    children,
    ...rest
  },
  ref,
) {
  return (
    <button
      ref={ref}
      className={clsx(
        styles.root,
        styles[`variant-${variant}`],
        styles[`size-${size}`],
        block && styles.block,
        loading && styles.loading,
        className,
      )}
      disabled={disabled ?? loading}
      {...rest}
    >
      {loading && <span className={styles.spinner} aria-hidden="true" />}
      {!loading && leftIcon && <span className={styles.iconLeft}>{leftIcon}</span>}
      <span className={styles.label}>{children}</span>
      {!loading && rightIcon && <span className={styles.iconRight}>{rightIcon}</span>}
    </button>
  );
});
