import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Bell, Send, CheckCheck } from 'lucide-react';

import {
  Badge,
  Button,
  Card,
  CardHeader,
  Input,
  Modal,
  PageHeader,
  Table,
  toast,
  type TableColumn,
} from '@shared/ui';

import { useDashboardStats } from '@features/dashboard/api';
import {
  useNotifications,
  useBroadcastNotification,
  type NotificationAdmin,
} from './api';
import styles from './NotificationsPage.module.css';

const broadcastSchema = z.object({
  title: z.string().min(1, 'Sarlavha kerak'),
  body: z.string().min(1, 'Matn kerak'),
});

type BroadcastValues = z.infer<typeof broadcastSchema>;

/** Bildirishnomalar boshqaruvi — ro'yxat + barcha foydalanuvchilarga xabar yuborish. */
export function NotificationsPage(): JSX.Element {
  const { data: items = [], isLoading } = useNotifications();
  const { data: stats } = useDashboardStats();
  const activeUsers = stats?.kpi.active_users ?? 0;
  const broadcast = useBroadcastNotification();
  const [broadcastOpen, setBroadcastOpen] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<BroadcastValues>({
    resolver: zodResolver(broadcastSchema),
    defaultValues: { title: '', body: '' },
  });

  const markAllRead = () => {
    toast.info("Bu funksiya keyingi versiyada tayyor bo'ladi");
  };

  const sendBroadcast = async (values: BroadcastValues) => {
    try {
      const result = await broadcast.mutateAsync(values);
      toast.success('Xabar yuborildi', `${result.sent_count} foydalanuvchiga`);
      setBroadcastOpen(false);
      reset({ title: '', body: '' });
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Yuborilmadi');
    }
  };

  const unreadCount = items.filter((n) => !n.is_read).length;

  const columns: TableColumn<NotificationAdmin>[] = [
    {
      header: '',
      width: '40px',
      cell: (n) => (
        <span className={`${styles.statusDot} ${n.is_read ? styles.dotRead : styles.dotUnread}`} />
      ),
    },
    {
      header: 'Sarlavha',
      width: '2fr',
      cell: (n) => (
        <div>
          <div className={styles.title}>{n.title}</div>
          <div className={styles.body}>{n.body}</div>
        </div>
      ),
    },
    {
      header: 'Holat',
      width: '1fr',
      cell: (n) => (
        <Badge tone={n.is_read ? 'neutral' : 'accent'}>
          {n.is_read ? "O'qilgan" : "Yangi"}
        </Badge>
      ),
    },
    {
      header: 'Yuborilgan',
      width: '1.2fr',
      cell: (n) => new Date(n.created_at).toLocaleString('uz-UZ'),
    },
  ];

  return (
    <>
      <PageHeader
        title="Bildirishnomalar"
        description={
          isLoading ? 'Yuklanmoqda…' : `Jami ${items.length} xabar, ${unreadCount} o'qilmagan`
        }
        actions={
          <>
            <Button variant="secondary" leftIcon={<CheckCheck size={16} />} onClick={markAllRead}>
              Hammasini o'qildi
            </Button>
            <Button leftIcon={<Send size={16} />} onClick={() => setBroadcastOpen(true)}>
              Xabar yuborish
            </Button>
          </>
        }
      />

      <Card className={styles.summaryCard}>
        <CardHeader
          title="Broadcast statistikasi"
          subtitle="Barcha foydalanuvchilar uchun statistika"
        />
        <div className={styles.stats}>
          <StatBlock label="Jami xabarlar" value={items.length} />
          <StatBlock label="Yangi" value={unreadCount} />
          <StatBlock label="O'qilgan" value={items.length - unreadCount} />
          <StatBlock label="Faol foydalanuvchi" value={activeUsers} />
        </div>
      </Card>

      <Table<NotificationAdmin>
        columns={columns}
        rows={items}
        loading={isLoading}
        keyExtractor={(n) => n.id}
        emptyState={
          <div className={styles.emptyBlock}>
            <Bell size={20} />
            <span>Hozircha bildirishnoma yo'q</span>
          </div>
        }
      />

      <Modal
        open={broadcastOpen}
        onClose={() => setBroadcastOpen(false)}
        title="Broadcast xabar"
        size="md"
        footer={
          <>
            <Button variant="ghost" onClick={() => setBroadcastOpen(false)}>
              Bekor
            </Button>
            <Button
              onClick={handleSubmit(sendBroadcast)}
              loading={isSubmitting}
              leftIcon={<Send size={16} />}
            >
              Yuborish
            </Button>
          </>
        }
      >
        <form onSubmit={handleSubmit(sendBroadcast)} className={styles.form}>
          <div className={styles.warning}>
            Bu xabar <strong>{activeUsers} foydalanuvchi</strong>ga (FCM push) yuboriladi
          </div>
          <Input
            label="Sarlavha"
            placeholder="Yangi retseptlar qo'shildi"
            {...(errors.title?.message ? { errorText: errors.title.message } : {})}
            {...register('title')}
          />
          <div className={styles.textareaWrap}>
            <label className={styles.textareaLabel}>Matn</label>
            <textarea
              className={styles.textarea}
              rows={4}
              placeholder="Menu Mate'ga 5 ta yangi milliy taom qo'shildi..."
              {...register('body')}
            />
            {errors.body?.message && (
              <div className={styles.errorText}>{errors.body.message}</div>
            )}
          </div>
        </form>
      </Modal>
    </>
  );
}

function StatBlock({ label, value }: { label: string; value: number }): JSX.Element {
  return (
    <div className={styles.statBlock}>
      <div className={styles.statLabel}>{label}</div>
      <div className={styles.statValue}>{value}</div>
    </div>
  );
}
