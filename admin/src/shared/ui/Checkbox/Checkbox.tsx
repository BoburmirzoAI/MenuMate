import { forwardRef, useId, type InputHTMLAttributes } from 'react';
import { Check } from 'lucide-react';
import clsx from 'clsx';

import styles from './Checkbox.module.css';

interface CheckboxProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}

/**
 * `<Checkbox>` — chiroyli checkbox (native input yashirin, custom vizual).
 *
 * ```tsx
 * <Checkbox label="Faol" checked={x} onChange={e => setX(e.target.checked)} />
 * ```
 */
export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(function Checkbox(
  { label, className, id, ...rest },
  ref,
) {
  const autoId = useId();
  const inputId = id ?? autoId;

  return (
    <label htmlFor={inputId} className={clsx(styles.root, className)}>
      <input ref={ref} id={inputId} type="checkbox" className={styles.input} {...rest} />
      <span className={styles.box}>
        <Check size={12} className={styles.check} />
      </span>
      {label && <span className={styles.label}>{label}</span>}
    </label>
  );
});
