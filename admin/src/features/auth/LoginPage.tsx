import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Mail, Lock, Eye, EyeOff, UtensilsCrossed } from 'lucide-react';

import { Button, Input } from '@shared/ui';
import { useAuthStore } from '@shared/auth/store';
import { ApiError } from '@shared/api/types';

import styles from './LoginPage.module.css';

/**
 * Login form uchun sxema.
 * Backend `EMAIL_ALREADY_EXISTS` va h.k. o'z xatolarini qaytaradi — biz faqat
 * mahalliy shakl validatsiyasini bajaramiz.
 */
const loginSchema = z.object({
  email: z.string().min(1, 'Email kiriting').email("Email formati noto'g'ri"),
  password: z.string().min(1, 'Parol kiriting'),
});

type LoginValues = z.infer<typeof loginSchema>;

/** Login sahifasi — brand chap panel + o'ngda form. */
export function LoginPage(): JSX.Element {
  const navigate = useNavigate();
  const location = useLocation();
  const login = useAuthStore((state) => state.login);
  const [serverError, setServerError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: '', password: '' },
  });

  const onSubmit = async (values: LoginValues) => {
    setServerError(null);
    try {
      await login(values.email, values.password);
      const from = (location.state as { from?: string } | null)?.from ?? '/';
      navigate(from, { replace: true });
    } catch (err) {
      const message =
        err instanceof ApiError
          ? err.message
          : "Kirish amalga oshmadi. Qayta urinib ko'ring.";
      setServerError(message);
    }
  };

  return (
    <div className={styles.root}>
      <aside className={styles.brand}>
        <div className={styles.brandInner}>
          <div className={styles.brandBadge}>
            <UtensilsCrossed size={24} />
          </div>
          <h1 className={styles.brandTitle}>Menu Mate</h1>
          <p className={styles.brandLead}>
            Oilaviy ovqat menyusini kuzatuvchi, retsept va bildirishnomalarni
            boshqaruvchi ichki panel.
          </p>
          <ul className={styles.brandList}>
            <li>Foydalanuvchi va oilalarni ko&#8216;rish</li>
            <li>35+ retsept, 73+ ingredient boshqaruvi</li>
            <li>Menyu, bayram va bildirishnomalarni sozlash</li>
          </ul>
        </div>
      </aside>

      <section className={styles.formSection}>
        <div className={styles.formCard}>
          <div className={styles.formHeader}>
            <h2 className={styles.formTitle}>Xush kelibsiz</h2>
            <p className={styles.formLead}>Akkauntingizga kiring va boshlang.</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className={styles.form} noValidate>
            <Input
              label="Email"
              type="email"
              autoComplete="email"
              placeholder="admin@menumate.uz"
              leftAdornment={<Mail size={16} />}
              {...(errors.email?.message ? { errorText: errors.email.message } : {})}
              {...register('email')}
            />

            <Input
              label="Parol"
              type={showPassword ? 'text' : 'password'}
              autoComplete="current-password"
              placeholder="••••••••"
              leftAdornment={<Lock size={16} />}
              rightAdornment={
                <button
                  type="button"
                  className={styles.eyeBtn}
                  onClick={() => setShowPassword((v) => !v)}
                  aria-label={showPassword ? "Parolni yashirish" : "Parolni ko'rsatish"}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              }
              {...(errors.password?.message ? { errorText: errors.password.message } : {})}
              {...register('password')}
            />

            {serverError && <div className={styles.serverError}>{serverError}</div>}

            <Button type="submit" variant="primary" size="lg" block loading={isSubmitting}>
              Kirish
            </Button>
          </form>

          <p className={styles.formHint}>
            Ushbu panel — <strong>Menu Mate</strong> loyihasining ichki admin qismi.
            Kirish uchun superuser akkaunt kerak.
          </p>
        </div>
      </section>
    </div>
  );
}
