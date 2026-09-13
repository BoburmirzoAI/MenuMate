import type { CSSProperties } from 'react';
import clsx from 'clsx';

import styles from './Skeleton.module.css';

interface SkeletonProps {
  width?: number | string;
  height?: number | string;
  radius?: number | string;
  className?: string;
}

/**
 * `<Skeleton>` — ma'lumot yuklanayotganda joyni to'ldiruvchi shimmer blok.
 *
 * ```tsx
 * <Skeleton width="100%" height={20} />
 * ```
 */
export function Skeleton({ width, height, radius, className }: SkeletonProps): JSX.Element {
  const style: CSSProperties = {
    width,
    height,
    borderRadius: radius,
  };
  return <div className={clsx(styles.root, className)} style={style} />;
}
