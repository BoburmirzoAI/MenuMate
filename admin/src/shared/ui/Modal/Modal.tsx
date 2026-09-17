import { useEffect, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';

import styles from './Modal.module.css';

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: ReactNode;
  /** Modal kengligi: sm/md/lg. Default md. */
  size?: 'sm' | 'md' | 'lg';
  /** Tashqariga bosilganda yopilishi. */
  closeOnBackdrop?: boolean;
  children: ReactNode;
  /** Pastki qism (odatda Cancel/Save tugmalar). */
  footer?: ReactNode;
}

/**
 * `<Modal>` — portal orqali `document.body`ga chiqadigan dialog.
 *
 * — `Escape` bosilganda yopiladi
 * — Body scroll modal ochilganda bloklanadi
 * — Backdrop bosilganda yopiladi (kerakli bo'lsa `closeOnBackdrop=false`)
 *
 * ```tsx
 * <Modal open={open} onClose={close} title="O'chirish?">
 *   ...content...
 * </Modal>
 * ```
 */
export function Modal({
  open,
  onClose,
  title,
  size = 'md',
  closeOnBackdrop = true,
  children,
  footer,
}: ModalProps): JSX.Element | null {
  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', onKey);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = prevOverflow;
    };
  }, [open, onClose]);

  if (!open) return null;

  return createPortal(
    <div
      className={styles.backdrop}
      onClick={() => closeOnBackdrop && onClose()}
      role="dialog"
      aria-modal="true"
    >
      <div
        className={`${styles.dialog} ${styles[`size-${size}`]}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className={styles.header}>
          <div className={styles.title}>{title}</div>
          <button className={styles.closeBtn} onClick={onClose} aria-label="Yopish">
            <X size={16} />
          </button>
        </div>
        <div className={styles.body}>{children}</div>
        {footer && <div className={styles.footer}>{footer}</div>}
      </div>
    </div>,
    document.body,
  );
}
