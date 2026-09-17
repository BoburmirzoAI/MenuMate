import { useState } from 'react';
import { Search, Smartphone, Apple, Globe, Bell, BellOff } from 'lucide-react';

import {
  Badge,
  Card,
  EmptyState,
  Input,
  PageHeader,
  Select,
  Table,
  type TableColumn,
} from '@shared/ui';

import { useDevices, type DeviceAdmin } from './api';
import styles from './DevicesPage.module.css';

const DEVICE_META: Record<
  DeviceAdmin['device_type'],
  { label: string; icon: React.ComponentType<{ size?: number }> }
> = {
  ANDROID: { label: 'Android', icon: Smartphone },
  IOS: { label: 'iOS', icon: Apple },
  WEB: { label: 'Web', icon: Globe },
};

/** Qurilmalar sahifasi — foydalanuvchi qurilmalari + FCM push token holati. */
export function DevicesPage(): JSX.Element {
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<'all' | DeviceAdmin['device_type']>('all');

  const params: Parameters<typeof useDevices>[0] = {};
  if (search) params.search = search;
  if (typeFilter !== 'all') params.device_type = typeFilter;
  const { data: devices = [], isLoading } = useDevices(params);

  const columns: TableColumn<DeviceAdmin>[] = [
    {
      header: 'Qurilma',
      width: '1.4fr',
      cell: (d) => {
        const meta = DEVICE_META[d.device_type];
        const Icon = meta.icon;
        return (
          <div className={styles.deviceCell}>
            <div className={styles.deviceIcon}>
              <Icon size={16} />
            </div>
            <div>
              <div className={styles.deviceLabel}>{meta.label}</div>
              <code className={styles.deviceId}>{d.device_id}</code>
            </div>
          </div>
        );
      },
    },
    {
      header: 'Foydalanuvchi',
      width: '2fr',
      cell: (d) => d.user_email,
    },
    {
      header: 'Versiya',
      width: '1fr',
      cell: (d) => <Badge tone="neutral">v{d.app_version}</Badge>,
    },
    {
      header: 'Push',
      width: '1fr',
      cell: (d) =>
        d.fcm_token_set ? (
          <Badge tone="success" dot>
            <Bell size={11} /> Yoqilgan
          </Badge>
        ) : (
          <Badge tone="neutral" dot>
            <BellOff size={11} /> O'chirilgan
          </Badge>
        ),
    },
    {
      header: 'Oxirgi aktivlik',
      width: '1.4fr',
      cell: (d) => new Date(d.last_login).toLocaleString('uz-UZ'),
    },
  ];

  const withFcm = devices.filter((d) => d.fcm_token_set).length;

  return (
    <>
      <PageHeader
        title="Qurilmalar"
        description={
          isLoading
            ? 'Yuklanmoqda…'
            : `${devices.length} qurilma, ${withFcm} tasi push xabarlarni oladi`
        }
      />

      <Card padded={false} className={styles.filterCard}>
        <div className={styles.filters}>
          <Input
            placeholder="Email yoki qurilma ID bo'yicha qidirish..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            leftAdornment={<Search size={16} />}
          />
          <Select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value as typeof typeFilter)}
            options={[
              { label: 'Barcha turlar', value: 'all' },
              { label: '📱 Android', value: 'ANDROID' },
              { label: '🍏 iOS', value: 'IOS' },
              { label: '🌐 Web', value: 'WEB' },
            ]}
          />
        </div>
      </Card>

      <Table<DeviceAdmin>
        columns={columns}
        rows={devices}
        loading={isLoading}
        keyExtractor={(d) => d.id}
        emptyState={
          <EmptyState
            icon={<Smartphone size={20} />}
            title="Qurilma topilmadi"
            description="Filterni o'zgartirib ko'ring"
          />
        }
      />
    </>
  );
}
