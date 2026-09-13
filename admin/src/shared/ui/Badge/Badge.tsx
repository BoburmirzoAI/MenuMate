import type { HTMLAttributes, ReactNode } from 'react';
import clsx from 'clsx';

import styles from './Badge.module.css';

export type BadgeTone = 'neutral' | 'accent' | 'success' | 'warning' | 'danger' | 'info';

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  tone?: BadgeTone;
  /** `dot` bo'lsa chap tomonda kichik nuqta chiqadi (status ko'rsatgich). */
  dot?: boolean;
  children: ReactNode;
}

/**
 * `<Badge>` — status yorlig'i (masalan "Faol", "Premium", "Cheklangan").
 */
export function Badge({ tone = 'neutral', dot = false, className, children, ...rest }: BadgeProps): JSX.Element {
  return (
    <span className={clsx(styles.root, styles[`tone-${tone}`], className)} {...rest}>
      {dot && <span className={styles.dot} />}
      {children}
    </span>
  );
}
