import type { ReactNode } from 'react';
import clsx from 'clsx';

import styles from './Table.module.css';

/** Bitta ustun ta'rifi. */
export interface TableColumn<T> {
  /** Ustun sarlavhasi. */
  header: ReactNode;
  /** Har row uchun mazmun hisoblab beruvchi funksiya. */
  cell: (row: T, index: number) => ReactNode;
  /** Ustun kengligini flexbox uchun (masalan `120px`, `1fr`). */
  width?: string;
  /** Matnni chapga/o'ngga tekislash. */
  align?: 'left' | 'right' | 'center';
}

interface TableProps<T> {
  columns: TableColumn<T>[];
  rows: T[];
  /** Row uchun barqaror key. */
  keyExtractor: (row: T, index: number) => string | number;
  /** Ma'lumot yuklanish holati (skeleton row'lar chiqadi). */
  loading?: boolean;
  /** Row bosilganda chaqiriladi (ixtiyoriy — click kerak bo'lmasa yozmang). */
  onRowClick?: (row: T) => void;
  /** Bo'sh holat mazmuni — odatda `<EmptyState />`. */
  emptyState?: ReactNode;
}

/**
 * `<Table>` — sodda va reactiv jadval.
 *
 * ```tsx
 * <Table
 *   rows={users}
 *   keyExtractor={(u) => u.id}
 *   columns={[
 *     { header: 'Email', cell: (u) => u.email, width: '2fr' },
 *     { header: 'Rol', cell: (u) => u.role, width: '1fr' },
 *   ]}
 * />
 * ```
 */
export function Table<T>({
  columns,
  rows,
  keyExtractor,
  loading = false,
  onRowClick,
  emptyState,
}: TableProps<T>): JSX.Element {
  const gridTemplate = columns.map((c) => c.width ?? '1fr').join(' ');

  if (loading) {
    return (
      <div className={styles.root}>
        <div className={styles.head} style={{ gridTemplateColumns: gridTemplate }}>
          {columns.map((col, i) => (
            <div
              key={i}
              className={clsx(styles.headCell, styles[`align-${col.align ?? 'left'}`])}
            >
              {col.header}
            </div>
          ))}
        </div>
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className={styles.row} style={{ gridTemplateColumns: gridTemplate }}>
            {columns.map((_col, j) => (
              <div key={j} className={styles.cell}>
                <div className={styles.skeletonBar} />
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  }

  if (rows.length === 0 && emptyState) {
    return (
      <div className={styles.root}>
        <div className={styles.head} style={{ gridTemplateColumns: gridTemplate }}>
          {columns.map((col, i) => (
            <div
              key={i}
              className={clsx(styles.headCell, styles[`align-${col.align ?? 'left'}`])}
            >
              {col.header}
            </div>
          ))}
        </div>
        <div className={styles.empty}>{emptyState}</div>
      </div>
    );
  }

  return (
    <div className={styles.root}>
      <div className={styles.head} style={{ gridTemplateColumns: gridTemplate }}>
        {columns.map((col, i) => (
          <div
            key={i}
            className={clsx(styles.headCell, styles[`align-${col.align ?? 'left'}`])}
          >
            {col.header}
          </div>
        ))}
      </div>
      {rows.map((row, rowIndex) => (
        <div
          key={keyExtractor(row, rowIndex)}
          className={clsx(styles.row, onRowClick && styles.rowClickable)}
          style={{ gridTemplateColumns: gridTemplate }}
          onClick={() => onRowClick?.(row)}
          role={onRowClick ? 'button' : undefined}
          tabIndex={onRowClick ? 0 : undefined}
        >
          {columns.map((col, colIndex) => (
            <div
              key={colIndex}
              className={clsx(styles.cell, styles[`align-${col.align ?? 'left'}`])}
            >
              {col.cell(row, rowIndex)}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
