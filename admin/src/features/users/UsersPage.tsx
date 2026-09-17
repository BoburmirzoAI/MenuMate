import { useState } from 'react';
import { Search, Ban, CheckCircle2, Trash2, ShieldCheck } from 'lucide-react';

import {
  Badge,
  Button,
  Card,
  EmptyState,
  Input,
  Modal,
  PageHeader,
  Select,
  Table,
  toast,
  type TableColumn,
} from '@shared/ui';
import type { User } from '@/types/domain';

import { useUsers, useUpdateUser, useDeleteUser } from './api';
import styles from './UsersPage.module.css';

type StatusFilter = 'all' | 'active' | 'blocked' | 'unverified';

/** Foydalanuvchilar boshqaruvi sahifasi. */
export function UsersPage(): JSX.Element {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [selected, setSelected] = useState<User | null>(null);

  const params: Parameters<typeof useUsers>[0] = { search };
  if (statusFilter !== 'all') params.status = statusFilter;
  const { data: users = [], isLoading } = useUsers(params);
  const updateUser = useUpdateUser();
  const deleteUser = useDeleteUser();

  const toggleActive = async (user: User) => {
    try {
      await updateUser.mutateAsync({ id: user.id, is_active: !user.is_active });
      toast.success(
        user.is_active ? 'Foydalanuvchi bloklandi' : 'Foydalanuvchi tiklandi',
        user.email,
      );
      setSelected(null);
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : "Bajarilmadi");
    }
  };

  const removeUser = async (user: User) => {
    try {
      await deleteUser.mutateAsync(user.id);
      toast.info("Foydalanuvchi o'chirildi", user.email);
      setSelected(null);
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : "O'chirilmadi");
    }
  };

  const columns: TableColumn<User>[] = [
    {
      header: 'Foydalanuvchi',
      width: '2.4fr',
      cell: (u) => (
        <div className={styles.userCell}>
          <div className={styles.avatar}>{u.first_name.charAt(0).toUpperCase()}</div>
          <div className={styles.userInfo}>
            <div className={styles.userName}>
              {u.first_name} {u.last_name}
            </div>
            <div className={styles.userEmail}>{u.email}</div>
          </div>
        </div>
      ),
    },
    {
      header: 'Rol',
      width: '1fr',
      cell: (u) => (
        <Badge tone={u.roles[0]?.codename === 'admin' ? 'accent' : 'neutral'}>
          {u.roles[0]?.name ?? '—'}
        </Badge>
      ),
    },
    {
      header: 'Holat',
      width: '1fr',
      cell: (u) => (
        <div className={styles.statusStack}>
          <Badge tone={u.is_active ? 'success' : 'danger'} dot>
            {u.is_active ? 'Faol' : 'Bloklangan'}
          </Badge>
          {u.is_premium && (
            <Badge tone="warning">Premium</Badge>
          )}
        </div>
      ),
    },
    {
      header: 'Email',
      width: '1fr',
      cell: (u) => (
        <Badge tone={u.is_email_verified ? 'success' : 'warning'}>
          {u.is_email_verified ? 'Tasdiqlangan' : 'Kutilmoqda'}
        </Badge>
      ),
    },
    {
      header: "Ro'yxatdan o'tgan",
      width: '1.2fr',
      cell: (u) => new Date(u.created_at).toLocaleDateString('uz-UZ'),
    },
  ];

  return (
    <>
      <PageHeader
        title="Foydalanuvchilar"
        description={isLoading ? 'Yuklanmoqda…' : `Ro'yxatdan o'tgan ${users.length} foydalanuvchi`}
      />

      <Card padded={false} className={styles.filterCard}>
        <div className={styles.filters}>
          <Input
            placeholder="Ism yoki email bo'yicha qidirish..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            leftAdornment={<Search size={16} />}
            className={styles.searchInput}
          />
          <Select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as StatusFilter)}
            options={[
              { label: 'Barcha holatlar', value: 'all' },
              { label: 'Faol', value: 'active' },
              { label: 'Bloklangan', value: 'blocked' },
              { label: 'Tasdiqlanmagan email', value: 'unverified' },
            ]}
            className={styles.statusSelect}
          />
        </div>
      </Card>

      <div className={styles.tableWrapper}>
        <Table<User>
          columns={columns}
          rows={users}
          loading={isLoading}
          keyExtractor={(u) => u.id}
          onRowClick={setSelected}
          emptyState={
            <EmptyState
              icon={<Search size={20} />}
              title="Hech narsa topilmadi"
              description="Qidiruv yoki filterni o'zgartirib ko'ring"
            />
          }
        />
      </div>

      <Modal
        open={selected !== null}
        onClose={() => setSelected(null)}
        title={selected ? `${selected.first_name} ${selected.last_name}` : ''}
        size="md"
        footer={
          selected && (
            <>
              <Button variant="ghost" onClick={() => setSelected(null)}>
                Bekor
              </Button>
              <Button
                variant={selected.is_active ? 'secondary' : 'primary'}
                leftIcon={selected.is_active ? <Ban size={16} /> : <CheckCircle2 size={16} />}
                onClick={() => toggleActive(selected)}
              >
                {selected.is_active ? 'Bloklash' : 'Tiklash'}
              </Button>
              <Button
                variant="danger"
                leftIcon={<Trash2 size={16} />}
                onClick={() => removeUser(selected)}
              >
                O'chirish
              </Button>
            </>
          )
        }
      >
        {selected && <UserDetails user={selected} />}
      </Modal>
    </>
  );
}

/** Modal ichidagi tafsilotlar. */
function UserDetails({ user }: { user: User }): JSX.Element {
  return (
    <div className={styles.details}>
      <DetailRow label="Email" value={user.email} />
      <DetailRow label="Telefon" value={user.phone || '—'} />
      <DetailRow label="Jinsi" value={user.gender === 'MALE' ? 'Erkak' : user.gender === 'FEMALE' ? 'Ayol' : '—'} />
      <DetailRow label="Vaqt mintaqasi" value={user.timezone} />
      <DetailRow
        label="Rol"
        value={
          <div className={styles.roleRow}>
            {user.roles.map((r) => (
              <Badge key={r.id} tone="accent">
                <ShieldCheck size={12} />
                {r.name}
              </Badge>
            ))}
          </div>
        }
      />
      <DetailRow
        label="Email holati"
        value={
          <Badge tone={user.is_email_verified ? 'success' : 'warning'}>
            {user.is_email_verified ? 'Tasdiqlangan' : 'Tasdiqlanmagan'}
          </Badge>
        }
      />
      <DetailRow
        label="Onboarding"
        value={
          <Badge tone={user.is_onboarded ? 'success' : 'neutral'}>
            {user.is_onboarded ? 'Yakunlangan' : 'Yakunlanmagan'}
          </Badge>
        }
      />
      <DetailRow
        label="Yaratilgan"
        value={new Date(user.created_at).toLocaleString('uz-UZ')}
      />
    </div>
  );
}

function DetailRow({
  label,
  value,
}: {
  label: string;
  value: React.ReactNode;
}): JSX.Element {
  return (
    <div className={styles.detailRow}>
      <div className={styles.detailLabel}>{label}</div>
      <div className={styles.detailValue}>{value}</div>
    </div>
  );
}
