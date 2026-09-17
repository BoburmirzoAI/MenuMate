import { createPortal } from 'react-dom';
import { CheckCircle, XCircle, Info, AlertTriangle, X } from 'lucide-react';

import { useToastStore } from './toastStore';

import styles from './ToastContainer.module.css';

const ICONS = {
  success: CheckCircle,
  error: XCircle,
  info: Info,
  warning: AlertTriangle,
};

/**
 * `<ToastContainer>` — App root'da bir marta joylashtiriladi, portal orqali chiqadi.
 * `toast.success(...)` chaqirilganda avtomatik ko'rinadi.
 */
export function ToastContainer(): JSX.Element {
  const items = useToastStore((state) => state.items);
  const dismiss = useToastStore((state) => state.dismiss);

  return createPortal(
    <div className={styles.root}>
      {items.map((item) => {
        const Icon = ICONS[item.tone];
        return (
          <div key={item.id} className={`${styles.toast} ${styles[`tone-${item.tone}`]}`}>
            <span className={styles.icon}>
              <Icon size={16} />
            </span>
            <div className={styles.body}>
              <div className={styles.title}>{item.title}</div>
              {item.description && <div className={styles.description}>{item.description}</div>}
            </div>
            <button
              className={styles.close}
              onClick={() => dismiss(item.id)}
              aria-label="Yopish"
            >
              <X size={14} />
            </button>
          </div>
        );
      })}
    </div>,
    document.body,
  );
}
