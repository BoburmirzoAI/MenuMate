import { useState } from 'react';
import { CalendarDays, Trash2 } from 'lucide-react';

import {
  Badge,
  Button,
  Card,
  EmptyState,
  Modal,
  PageHeader,
  Select,
  Table,
  toast,
  type TableColumn,
} from '@shared/ui';

import { useMenus, useDeleteMenu, type MenuAdmin } from './api';
import styles from './MenusPage.module.css';

/** Menyular boshqaruvi — barcha foydalanuvchilarning menyulari. */
export function MenusPage(): JSX.Element {
  const [statusFilter, setStatusFilter] = useState<'all' | 'ACTIVE' | 'COMPLETED'>('all');
  const [selected, setSelected] = useState<MenuAdmin | null>(null);

  const { data: menus = [], isLoading } = useMenus(
    statusFilter === 'all' ? undefined : statusFilter,
  );
  const deleteMenu = useDeleteMenu();

  const removeMenu = async (menu: MenuAdmin) => {
    try {
      await deleteMenu.mutateAsync(menu.id);
      toast.info("Menyu o'chirildi", `#${menu.id}`);
      setSelected(null);
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : "O'chirilmadi");
    }
  };

  const columns: TableColumn<MenuAdmin>[] = [
    {
      header: 'ID',
      width: '80px',
      cell: (m) => <code className={styles.code}>#{m.id}</code>,
    },
    {
      header: 'Oila',
      width: '2fr',
      cell: (m) => (
        <div>
          <div>{m.family_name || `Oila #${m.family}`}</div>
          <div style={{ fontSize: 11, color: 'var(--color-text-muted)' }}>{m.owner_email}</div>
        </div>
      ),
    },
    {
      header: 'Davomiylik',
      width: '1fr',
      cell: (m) => (
        <Badge tone="accent">{m.duration === 'WEEKLY' ? '7 kun' : '30 kun'}</Badge>
      ),
    },
    {
      header: 'Sana oralig\'i',
      width: '1.6fr',
      cell: (m) => (
        <span className={styles.dateRange}>
          {new Date(m.start_date).toLocaleDateString('uz-UZ')} —{' '}
          {new Date(m.end_date).toLocaleDateString('uz-UZ')}
        </span>
      ),
    },
    {
      header: 'Holat',
      width: '1fr',
      cell: (m) => (
        <Badge tone={m.status === 'ACTIVE' ? 'success' : 'neutral'} dot>
          {m.status === 'ACTIVE' ? 'Faol' : 'Tugallangan'}
        </Badge>
      ),
    },
    {
      header: 'Yaratilgan',
      width: '1.2fr',
      cell: (m) => new Date(m.created_at).toLocaleDateString('uz-UZ'),
    },
  ];

  return (
    <>
      <PageHeader
        title="Menyular"
        description={
          isLoading ? 'Yuklanmoqda…' : `Barcha foydalanuvchilarning ${menus.length} menyusi`
        }
      />

      <Card padded={false} className={styles.filterCard}>
        <Select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value as typeof statusFilter)}
          options={[
            { label: 'Barcha holatlar', value: 'all' },
            { label: 'Faol', value: 'ACTIVE' },
            { label: 'Tugallangan', value: 'COMPLETED' },
          ]}
          className={styles.statusFilter}
        />
      </Card>

      <Table<MenuAdmin>
        columns={columns}
        rows={menus}
        loading={isLoading}
        keyExtractor={(m) => m.id}
        onRowClick={setSelected}
        emptyState={
          <EmptyState
            icon={<CalendarDays size={20} />}
            title="Menyu topilmadi"
            description="Boshqa filter tanlab ko'ring"
          />
        }
      />

      <Modal
        open={selected !== null}
        onClose={() => setSelected(null)}
        title={selected ? `Menyu #${selected.id}` : ''}
        size="md"
        footer={
          selected && (
            <>
              <Button variant="ghost" onClick={() => setSelected(null)}>
                Yopish
              </Button>
              <Button
                variant="danger"
                leftIcon={<Trash2 size={16} />}
                onClick={() => removeMenu(selected)}
              >
                O'chirish
              </Button>
            </>
          )
        }
      >
        {selected && (
          <div className={styles.details}>
            <DetailRow
              label="Oila"
              value={selected.family_name || `Oila #${selected.family}`}
            />
            <DetailRow
              label="Davomiylik"
              value={
                <Badge tone="accent">
                  {selected.duration === 'WEEKLY' ? '7 kun (haftalik)' : '30 kun (oylik)'}
                </Badge>
              }
            />
            <DetailRow
              label="Boshlanish"
              value={new Date(selected.start_date).toLocaleDateString('uz-UZ')}
            />
            <DetailRow
              label="Tugash"
              value={new Date(selected.end_date).toLocaleDateString('uz-UZ')}
            />
            <DetailRow
              label="Holat"
              value={
                <Badge tone={selected.status === 'ACTIVE' ? 'success' : 'neutral'} dot>
                  {selected.status === 'ACTIVE' ? 'Faol' : 'Tugallangan'}
                </Badge>
              }
            />
            {selected.notes && <DetailRow label="Eslatma" value={selected.notes} />}
            <DetailRow
              label="Yaratilgan"
              value={new Date(selected.created_at).toLocaleString('uz-UZ')}
            />
          </div>
        )}
      </Modal>
    </>
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
