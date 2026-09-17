import { useEffect, useState } from 'react';
import { UserPlus, User as UserIcon, KeyRound, Shield } from 'lucide-react';

import {
  Badge,
  Button,
  Checkbox,
  Input,
  Modal,
  Select,
  toast,
} from '@shared/ui';
import type { User } from '@/types/domain';
import { useRoles } from '@features/permissions/api';

import {
  useCreateUser,
  useUpdateUser,
  useSetUserPassword,
  type UserCreatePayload,
  type UserUpdatePayload,
} from './api';
import styles from './UserFormModal.module.css';

interface UserFormModalProps {
  open: boolean;
  onClose: () => void;
  /** null → create rejimi, User → edit rejimi. */
  user: User | null;
}

interface FormState {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  gender: '' | 'MALE' | 'FEMALE';
  timezone: string;
  language: 'uz' | 'ru' | 'en';
  is_active: boolean;
  is_email_verified: boolean;
  is_push_enabled: boolean;
}

const initialState: FormState = {
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  phone_number: '',
  gender: '',
  timezone: 'Asia/Tashkent',
  language: 'uz',
  is_active: true,
  is_email_verified: false,
  is_push_enabled: true,
};

/**
 * Foydalanuvchi CRUD modal — bir komponent orqali:
 * - Yangi user yaratish (parol maydoni bilan)
 * - Mavjud user'ni tahrirlash (parol alohida "Parolni o'zgartirish" bo'limida)
 */
export function UserFormModal({ open, onClose, user }: UserFormModalProps): JSX.Element {
  const isEdit = user !== null;
  const [form, setForm] = useState<FormState>(initialState);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [newPassword, setNewPassword] = useState('');
  const [roleIds, setRoleIds] = useState<Set<number>>(new Set());

  const createUser = useCreateUser();
  const updateUser = useUpdateUser();
  const setPassword = useSetUserPassword();
  const { data: allRoles = [] } = useRoles();

  // User o'zgarganda formni to'ldirish
  useEffect(() => {
    if (!open) return;
    if (user) {
      setForm({
        email: user.email,
        password: '',
        first_name: user.first_name ?? '',
        last_name: user.last_name ?? '',
        phone_number: user.phone ?? '',
        gender: (user.gender as '' | 'MALE' | 'FEMALE') ?? '',
        timezone: user.timezone ?? 'Asia/Tashkent',
        language: 'uz',
        is_active: user.is_active,
        is_email_verified: user.is_email_verified,
        is_push_enabled: true,
      });
      setRoleIds(new Set((user.roles ?? []).map((r) => r.id)));
    } else {
      setForm(initialState);
      setRoleIds(new Set());
    }
    setErrors({});
    setNewPassword('');
  }, [open, user]);

  const toggleRole = (id: number) =>
    setRoleIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  const update = <K extends keyof FormState>(key: K, value: FormState[K]) => {
    setForm((f) => ({ ...f, [key]: value }));
    setErrors((e) => ({ ...e, [key]: '' }));
  };

  const validate = (): boolean => {
    const errs: Record<string, string> = {};
    if (!isEdit) {
      if (!form.email.trim()) errs.email = 'Email kerak';
      else if (!form.email.includes('@')) errs.email = "Email formati noto'g'ri";
      if (form.password.length < 6) errs.password = 'Kamida 6 belgi';
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;
    try {
      if (isEdit && user) {
        const payload: UserUpdatePayload = {
          id: user.id,
          first_name: form.first_name,
          last_name: form.last_name,
          phone_number: form.phone_number,
          timezone: form.timezone,
          language: form.language,
          is_active: form.is_active,
          is_email_verified: form.is_email_verified,
          is_push_enabled: form.is_push_enabled,
          role_ids: Array.from(roleIds),
        };
        if (form.gender) payload.gender = form.gender;
        await updateUser.mutateAsync(payload);
        toast.success("Ma'lumot yangilandi", user.email);
      } else {
        const payload: UserCreatePayload = {
          email: form.email.trim().toLowerCase(),
          password: form.password,
          first_name: form.first_name,
          last_name: form.last_name,
          phone_number: form.phone_number,
          timezone: form.timezone,
          language: form.language,
          is_active: form.is_active,
          is_email_verified: form.is_email_verified,
          is_push_enabled: form.is_push_enabled,
          role_ids: Array.from(roleIds),
        };
        if (form.gender) payload.gender = form.gender;
        await createUser.mutateAsync(payload);
        toast.success("Yangi foydalanuvchi qo'shildi", form.email);
      }
      onClose();
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Bajarilmadi');
    }
  };

  const handleChangePassword = async () => {
    if (!user) return;
    if (newPassword.length < 6) {
      toast.error('Xato', 'Parol kamida 6 belgi');
      return;
    }
    try {
      await setPassword.mutateAsync({ id: user.id, password: newPassword });
      toast.success("Parol o'zgartirildi", user.email);
      setNewPassword('');
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : "O'zgartirilmadi");
    }
  };

  const submitting = createUser.isPending || updateUser.isPending;

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={
        <span className={styles.modalTitle}>
          {isEdit ? <UserIcon size={16} /> : <UserPlus size={16} />}
          {isEdit ? "Foydalanuvchi tahriri" : "Yangi foydalanuvchi"}
        </span>
      }
      size="lg"
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Bekor
          </Button>
          <Button onClick={handleSubmit} loading={submitting}>
            {isEdit ? 'Saqlash' : "Qo'shish"}
          </Button>
        </>
      }
    >
      <div className={styles.form}>
        {!isEdit && (
          <>
            <div className={styles.section}>
              <div className={styles.sectionTitle}>Kirish ma'lumotlari</div>
              <div className={styles.row}>
                <Input
                  label="Email *"
                  value={form.email}
                  onChange={(e) => update('email', e.target.value)}
                  placeholder="user@menumate.uz"
                  {...(errors.email ? { errorText: errors.email } : {})}
                />
                <Input
                  label="Parol *"
                  type="password"
                  value={form.password}
                  onChange={(e) => update('password', e.target.value)}
                  placeholder="Kamida 6 belgi"
                  {...(errors.password ? { errorText: errors.password } : {})}
                />
              </div>
            </div>
          </>
        )}

        {isEdit && user && (
          <div className={styles.emailReadonly}>
            <div className={styles.emailLabel}>Email</div>
            <div className={styles.emailValue}>{user.email}</div>
            <Badge tone="neutral">O'zgartirib bo'lmaydi</Badge>
          </div>
        )}

        <div className={styles.section}>
          <div className={styles.sectionTitle}>Shaxsiy ma'lumotlar</div>
          <div className={styles.row}>
            <Input
              label="Ism"
              value={form.first_name}
              onChange={(e) => update('first_name', e.target.value)}
              placeholder="Boburmirzo"
            />
            <Input
              label="Familiya"
              value={form.last_name}
              onChange={(e) => update('last_name', e.target.value)}
              placeholder="Sobirjanov"
            />
          </div>
          <div className={styles.row}>
            <Input
              label="Telefon"
              value={form.phone_number}
              onChange={(e) => update('phone_number', e.target.value)}
              placeholder="+998 90 123 45 67"
            />
            <Select
              label="Jinsi"
              value={form.gender}
              onChange={(e) => update('gender', e.target.value as FormState['gender'])}
              options={[
                { label: 'Tanlanmagan', value: '' },
                { label: 'Erkak', value: 'MALE' },
                { label: 'Ayol', value: 'FEMALE' },
              ]}
            />
          </div>
        </div>

        <div className={styles.section}>
          <div className={styles.sectionTitle}>Til va vaqt mintaqasi</div>
          <div className={styles.row}>
            <Select
              label="Til"
              value={form.language}
              onChange={(e) => update('language', e.target.value as FormState['language'])}
              options={[
                { label: "🇺🇿 O'zbek", value: 'uz' },
                { label: '🇷🇺 Русский', value: 'ru' },
                { label: '🇬🇧 English', value: 'en' },
              ]}
            />
            <Input
              label="Vaqt mintaqasi"
              value={form.timezone}
              onChange={(e) => update('timezone', e.target.value)}
              placeholder="Asia/Tashkent"
            />
          </div>
        </div>

        <div className={styles.section}>
          <div className={styles.sectionTitle}>
            <Shield size={14} /> Rollar (RBAC)
          </div>
          {allRoles.length === 0 ? (
            <div style={{ fontSize: 13, color: 'var(--color-text-muted)' }}>
              Hech qanday rol topilmadi. "Rollar va ruxsatlar" sahifasida yarating.
            </div>
          ) : (
            <div className={styles.checkboxes}>
              {allRoles.map((r) => (
                <label
                  key={r.id}
                  style={{ display: 'inline-flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}
                >
                  <Checkbox
                    checked={roleIds.has(r.id)}
                    onChange={() => toggleRole(r.id)}
                  />
                  <span>{r.name}</span>
                  <Badge tone="neutral">{r.permission_ids.length}</Badge>
                </label>
              ))}
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionTitle}>Sozlamalar</div>
          <div className={styles.checkboxes}>
            <Checkbox
              label="Faol foydalanuvchi"
              checked={form.is_active}
              onChange={(e) => update('is_active', e.target.checked)}
            />
            <Checkbox
              label="Email tasdiqlangan"
              checked={form.is_email_verified}
              onChange={(e) => update('is_email_verified', e.target.checked)}
            />
            <Checkbox
              label="Push xabar yoqilgan"
              checked={form.is_push_enabled}
              onChange={(e) => update('is_push_enabled', e.target.checked)}
            />
          </div>
        </div>

        {isEdit && user && (
          <div className={styles.section}>
            <div className={styles.sectionTitle}>
              <KeyRound size={14} /> Parolni o'zgartirish
            </div>
            <div className={styles.passwordRow}>
              <Input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="Yangi parol (kamida 6 belgi)"
              />
              <Button
                variant="secondary"
                onClick={handleChangePassword}
                loading={setPassword.isPending}
                disabled={!newPassword}
              >
                O'zgartirish
              </Button>
            </div>
          </div>
        )}
      </div>
    </Modal>
  );
}
