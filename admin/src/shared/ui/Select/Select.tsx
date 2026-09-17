import { forwardRef, useId, type SelectHTMLAttributes } from 'react';
import clsx from 'clsx';
import { ChevronDown } from 'lucide-react';

import styles from './Select.module.css';

export interface SelectOption {
  label: string;
  value: string;
}

export interface SelectProps extends Omit<SelectHTMLAttributes<HTMLSelectElement>, 'size'> {
  label?: string;
  hint?: string;
  errorText?: string;
  options: SelectOption[];
  placeholder?: string;
}

/**
 * `<Select>` — native `<select>` ustidan chiroyli qobiq.
 *
 * ```tsx
 * <Select label="Rol" options={[
 *   { label: 'Admin', value: 'ADMIN' },
 *   { label: 'User', value: 'USER' },
 * ]} />
 * ```
 */
export const Select = forwardRef<HTMLSelectElement, SelectProps>(function Select(
  { label, hint, errorText, options, placeholder, id, className, ...rest },
  ref,
) {
  const autoId = useId();
  const selectId = id ?? autoId;
  const invalid = Boolean(errorText);

  return (
    <div className={clsx(styles.root, className)}>
      {label && (
        <label htmlFor={selectId} className={styles.label}>
          {label}
        </label>
      )}
      <div className={clsx(styles.field, invalid && styles.invalid)}>
        <select ref={ref} id={selectId} className={styles.select} {...rest}>
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        <ChevronDown size={16} className={styles.chevron} />
      </div>
      {errorText ? (
        <p className={styles.error}>{errorText}</p>
      ) : hint ? (
        <p className={styles.hint}>{hint}</p>
      ) : null}
    </div>
  );
});
