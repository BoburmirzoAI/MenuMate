import { useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Plus, PartyPopper, Trash2, Pencil } from 'lucide-react';

import {
  Badge,
  Button,
  Card,
  Checkbox,
  Input,
  Modal,
  PageHeader,
  Table,
  toast,
  type TableColumn,
} from '@shared/ui';

import {
  useHolidays,
  useCreateHoliday,
  useUpdateHoliday,
  useDeleteHoliday,
  type HolidayAdmin,
} from './api';
import styles from './HolidaysPage.module.css';

const schema = z.object({
  name: z.string().min(1, 'Nomi kerak'),
  month: z.number().min(1).max(12),
  day: z.number().min(1).max(31),
  is_movable: z.boolean(),
});

type FormValues = z.infer<typeof schema>;

/** Bayramlar boshqaruvi — CRUD. */
export function HolidaysPage(): JSX.Element {
  const { data: holidays = [], isLoading } = useHolidays();
  const createHoliday = useCreateHoliday();
  const updateHoliday = useUpdateHoliday();
  const deleteHoliday = useDeleteHoliday();
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<HolidayAdmin | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', month: 1, day: 1, is_movable: false },
  });

  const openCreate = () => {
    setEditing(null);
    reset({ name: '', month: 1, day: 1, is_movable: false });
    setModalOpen(true);
  };

  const openEdit = (holiday: HolidayAdmin) => {
    setEditing(holiday);
    reset({
      name: holiday.name,
      month: holiday.month,
      day: holiday.day,
      is_movable: holiday.is_movable,
    });
    setModalOpen(true);
  };

  const removeHoliday = async (h: HolidayAdmin) => {
    try {
      await deleteHoliday.mutateAsync(h.id);
      toast.info("Bayram o'chirildi", h.name);
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : "O'chirilmadi");
    }
  };

  const onSubmit = async (values: FormValues) => {
    try {
      if (editing) {
        await updateHoliday.mutateAsync({ id: editing.id, ...values });
        toast.success('Bayram yangilandi', values.name);
      } else {
        await createHoliday.mutateAsync(values);
        toast.success("Yangi bayram qo'shildi", values.name);
      }
      setModalOpen(false);
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Saqlanmadi');
    }
  };

  const sorted = useMemo(
    () => [...holidays].sort((a, b) => a.month - b.month || a.day - b.day),
    [holidays],
  );

  const columns: TableColumn<HolidayAdmin>[] = [
    { header: 'Nomi', width: '2.5fr', cell: (h) => <strong>{h.name}</strong> },
    {
      header: 'Sana',
      width: '1fr',
      cell: (h) => `${h.day.toString().padStart(2, '0')}.${h.month.toString().padStart(2, '0')}`,
    },
    {
      header: 'Turi',
      width: '1fr',
      cell: (h) => (
        <Badge tone={h.is_movable ? 'warning' : 'accent'}>
          {h.is_movable ? "Ko'chuvchi" : 'Aniq sana'}
        </Badge>
      ),
    },
    {
      header: '',
      width: '120px',
      align: 'right',
      cell: (h) => (
        <div className={styles.actions}>
          <button
            className={styles.iconBtn}
            onClick={(e) => {
              e.stopPropagation();
              openEdit(h);
            }}
            aria-label="Tahrirlash"
          >
            <Pencil size={14} />
          </button>
          <button
            className={styles.iconBtnDanger}
            onClick={(e) => {
              e.stopPropagation();
              removeHoliday(h);
            }}
            aria-label="O'chirish"
          >
            <Trash2 size={14} />
          </button>
        </div>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Bayramlar"
        description={isLoading ? 'Yuklanmoqda…' : `${holidays.length} bayram — kalendar bo'yicha`}
        actions={
          <Button leftIcon={<Plus size={16} />} onClick={openCreate}>
            Yangi bayram
          </Button>
        }
      />

      <Table<HolidayAdmin>
        columns={columns}
        rows={sorted}
        loading={isLoading}
        keyExtractor={(h) => h.id}
        emptyState={
          <Card padded={false}>
            <div className={styles.emptyBlock}>
              <PartyPopper size={20} />
              <div>Bayramlar yo'q. Yangi bayram qo'shing.</div>
            </div>
          </Card>
        }
      />

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editing ? 'Bayramni tahrirlash' : 'Yangi bayram'}
        size="sm"
        footer={
          <>
            <Button variant="ghost" onClick={() => setModalOpen(false)}>
              Bekor
            </Button>
            <Button onClick={handleSubmit(onSubmit)}>Saqlash</Button>
          </>
        }
      >
        <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
          <Input
            label="Bayram nomi"
            placeholder="Masalan: Yangi yil"
            {...(errors.name?.message ? { errorText: errors.name.message } : {})}
            {...register('name')}
          />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input
              label="Kun"
              type="number"
              min={1}
              max={31}
              {...(errors.day?.message ? { errorText: errors.day.message } : {})}
              {...register('day', { valueAsNumber: true })}
            />
            <Input
              label="Oy"
              type="number"
              min={1}
              max={12}
              {...(errors.month?.message ? { errorText: errors.month.message } : {})}
              {...register('month', { valueAsNumber: true })}
            />
          </div>
          <Checkbox label="Ko'chuvchi bayram (masalan Ramazon hayiti)" {...register('is_movable')} />
        </form>
      </Modal>
    </>
  );
}
