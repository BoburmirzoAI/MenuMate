import { useEffect, useMemo, useState } from 'react';
import { UsersRound, Plus, Pencil, Search } from 'lucide-react';

import { Button, Input, Modal, toast } from '@shared/ui';
import { useUsers } from '@features/users/api';

import {
  useCreateFamily,
  useUpdateFamily,
  useFamilies,
  type FamilyListItem,
} from './api';
import styles from './FamilyFormModal.module.css';

interface FamilyFormModalProps {
  open: boolean;
  onClose: () => void;
  /** null → create, FamilyListItem → edit. */
  family: FamilyListItem | null;
}

/** Oila yaratish yoki tahrirlash modali — foydalanuvchini qidirish orqali tanlash. */
export function FamilyFormModal({
  open,
  onClose,
  family,
}: FamilyFormModalProps): JSX.Element {
  const isEdit = family !== null;
  const [familyName, setFamilyName] = useState('');
  const [city, setCity] = useState('');
  const [userId, setUserId] = useState<number | null>(null);
  const [userSearch, setUserSearch] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const createFamily = useCreateFamily();
  const updateFamily = useUpdateFamily();

  // Foydalanuvchilar ro'yxati — faqat create rejimida kerak
  const { data: users = [], isLoading: usersLoading } = useUsers({
    ...(userSearch.trim() ? { search: userSearch.trim() } : {}),
  });
  const { data: families = [] } = useFamilies();

  // Oilasi bor foydalanuvchilarni email bo'yicha chiqarib tashlaymiz (OneToOne)
  const emailsWithFamily = useMemo(
    () => new Set(families.map((f) => f.owner_email)),
    [families],
  );

  const availableUsers = useMemo(
    () => users.filter((u) => !emailsWithFamily.has(u.email)),
    [users, emailsWithFamily],
  );

  useEffect(() => {
    if (!open) return;
    if (family) {
      setFamilyName(family.family_name);
      setCity(family.city);
    } else {
      setFamilyName('');
      setCity('Tashkent');
    }
    setUserId(null);
    setUserSearch('');
    setErrors({});
  }, [open, family]);

  const handleSubmit = async () => {
    const errs: Record<string, string> = {};
    if (!familyName.trim()) errs.familyName = 'Oila nomi kerak';
    if (!city.trim()) errs.city = 'Shahar kerak';
    if (!isEdit && !userId) errs.userId = 'Foydalanuvchini tanlang';
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;

    try {
      if (isEdit && family) {
        await updateFamily.mutateAsync({
          id: family.id,
          family_name: familyName,
          city,
        });
        toast.success("Oila ma'lumoti yangilandi", familyName);
      } else {
        await createFamily.mutateAsync({
          user_id: userId!,
          family_name: familyName,
          city,
        });
        toast.success("Yangi oila qo'shildi", familyName);
      }
      onClose();
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Bajarilmadi');
    }
  };

  const submitting = createFamily.isPending || updateFamily.isPending;

  const selectedUser = useMemo(
    () => users.find((u) => u.id === userId) ?? null,
    [users, userId],
  );

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 8 }}>
          {isEdit ? <Pencil size={16} /> : <Plus size={16} />}
          {isEdit ? 'Oilani tahrirlash' : 'Yangi oila'}
        </span>
      }
      size="sm"
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
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {!isEdit && (
          <div className={styles.userPicker}>
            <div className={styles.pickerLabel}>Foydalanuvchi *</div>
            {selectedUser ? (
              <div className={styles.selectedUser}>
                <div className={styles.selectedAvatar}>
                  {(selectedUser.first_name?.[0] ?? selectedUser.email[0] ?? '?').toUpperCase()}
                </div>
                <div className={styles.selectedInfo}>
                  <div className={styles.selectedName}>
                    {selectedUser.first_name || selectedUser.last_name
                      ? `${selectedUser.first_name} ${selectedUser.last_name}`.trim()
                      : selectedUser.email}
                  </div>
                  <div className={styles.selectedEmail}>{selectedUser.email}</div>
                </div>
                <button
                  type="button"
                  className={styles.changeBtn}
                  onClick={() => setUserId(null)}
                >
                  O'zgartirish
                </button>
              </div>
            ) : (
              <>
                <Input
                  placeholder="Email yoki ism bo'yicha qidirish..."
                  value={userSearch}
                  onChange={(e) => setUserSearch(e.target.value)}
                  leftAdornment={<Search size={14} />}
                  {...(errors.userId ? { errorText: errors.userId } : {})}
                />
                <div className={styles.userList}>
                  {usersLoading ? (
                    <div className={styles.userListEmpty}>Yuklanmoqda…</div>
                  ) : availableUsers.length === 0 ? (
                    <div className={styles.userListEmpty}>
                      {userSearch
                        ? 'Foydalanuvchi topilmadi'
                        : 'Oilasiz foydalanuvchi qolmagan'}
                    </div>
                  ) : (
                    availableUsers.slice(0, 30).map((u) => (
                      <button
                        key={u.id}
                        type="button"
                        className={styles.userRow}
                        onClick={() => {
                          setUserId(u.id);
                          setErrors((prev) => {
                            const { userId: _u, ...rest } = prev;
                            return rest;
                          });
                        }}
                      >
                        <div className={styles.userAvatar}>
                          {(u.first_name?.[0] ?? u.email[0] ?? '?').toUpperCase()}
                        </div>
                        <div className={styles.userInfo}>
                          <div className={styles.userName}>
                            {u.first_name || u.last_name
                              ? `${u.first_name} ${u.last_name}`.trim()
                              : u.email}
                          </div>
                          <div className={styles.userEmail}>{u.email}</div>
                        </div>
                        <div className={styles.userId}>#{u.id}</div>
                      </button>
                    ))
                  )}
                </div>
              </>
            )}
          </div>
        )}
        <Input
          label="Oila nomi *"
          value={familyName}
          onChange={(e) => setFamilyName(e.target.value)}
          placeholder="Sobirjonov oilasi"
          leftAdornment={<UsersRound size={16} />}
          {...(errors.familyName ? { errorText: errors.familyName } : {})}
        />
        <Input
          label="Shahar *"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Tashkent"
          hint="OpenWeatherMap uchun shahar nomi (Tashkent, Samarkand, ...)"
          {...(errors.city ? { errorText: errors.city } : {})}
        />
      </div>
    </Modal>
  );
}
