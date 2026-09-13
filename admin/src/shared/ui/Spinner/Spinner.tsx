import clsx from 'clsx';

import styles from './Spinner.module.css';

interface SpinnerProps {
  size?: number;
  className?: string;
  /** Ekran o'quvchi uchun matn (default: "Yuklanmoqda"). */
  label?: string;
}

/**
 * `<Spinner>` — aylanuvchi yuklanish indikatori.
 *
 * ```tsx
 * <Spinner size={20} />
 * ```
 */
export function Spinner({ size = 16, className, label = 'Yuklanmoqda' }: SpinnerProps): JSX.Element {
  return (
    <span
      className={clsx(styles.root, className)}
      style={{ width: size, height: size }}
      role="status"
      aria-label={label}
    />
  );
}
