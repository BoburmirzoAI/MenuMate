import { forwardRef, useId, type InputHTMLAttributes, type ReactNode } from 'react';
import clsx from 'clsx';

import styles from './Input.module.css';

export interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string;
  hint?: string;
  errorText?: string;
  /** Chap tomonga (masalan, ikon yoki `@`) qo'yiladigan element. */
  leftAdornment?: ReactNode;
  /** O'ng tomonga (masalan, `toggle password`) qo'yiladigan element. */
  rightAdornment?: ReactNode;
}

/**
 * `<Input>` — form input'i.
 *
 * ```tsx
 * <Input label="Email" type="email" leftAdornment={<Mail size={16} />} />
 * <Input errorText="Parol xato" type="password" />
 * ```
 */
export const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  { label, hint, errorText, leftAdornment, rightAdornment, id, className, ...rest },
  ref,
) {
  const autoId = useId();
  const inputId = id ?? autoId;
  const invalid = Boolean(errorText);

  return (
    <div className={clsx(styles.root, className)}>
      {label && (
        <label htmlFor={inputId} className={styles.label}>
          {label}
        </label>
      )}
      <div className={clsx(styles.field, invalid && styles.invalid)}>
        {leftAdornment && <span className={styles.adornmentLeft}>{leftAdornment}</span>}
        <input
          ref={ref}
          id={inputId}
          className={styles.input}
          aria-invalid={invalid}
          aria-describedby={errorText ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
          {...rest}
        />
        {rightAdornment && <span className={styles.adornmentRight}>{rightAdornment}</span>}
      </div>
      {errorText ? (
        <p id={`${inputId}-error`} className={styles.error}>
          {errorText}
        </p>
      ) : hint ? (
        <p id={`${inputId}-hint`} className={styles.hint}>
          {hint}
        </p>
      ) : null}
    </div>
  );
});
