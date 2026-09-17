import { Cloud, RefreshCw, Sun, CloudRain, Wind, Trash2 } from 'lucide-react';

import {
  Badge,
  Button,
  Card,
  CardHeader,
  EmptyState,
  PageHeader,
  Spinner,
  toast,
} from '@shared/ui';

import { useWeatherSnapshots, useClearWeatherCache } from './api';
import styles from './WeatherPage.module.css';

/**
 * Ob-havo cache holati sahifasi.
 *
 * Backend `WeatherSnapshot` jadvalidan oxirgi yozuvlarni ko'rsatadi va admin
 * "Cache tozalash" tugmasi bilan hammasini nol qilib qo'yadi.
 */
export function WeatherPage(): JSX.Element {
  const { data: snapshots = [], isLoading } = useWeatherSnapshots();
  const clearCache = useClearWeatherCache();

  const clearAll = async () => {
    if (!window.confirm('Barcha ob-havo cache yozuvlari o‘chiriladi. Davom etamizmi?')) return;
    try {
      await clearCache.mutateAsync();
      toast.success('Cache tozalandi');
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Tozalanmadi');
    }
  };

  const iconFor = (description: string) => {
    const desc = description.toLowerCase();
    if (desc.includes('rain') || desc.includes('yog')) return CloudRain;
    if (desc.includes('cloud') || desc.includes('bulut')) return Cloud;
    return Sun;
  };

  return (
    <>
      <PageHeader
        title="Ob-havo cache"
        description={
          isLoading
            ? 'Yuklanmoqda…'
            : `OpenWeatherMap ma'lumotlari — Redis'da 3 soat, DB'da so'nggi ${snapshots.length} yozuv`
        }
        actions={
          <Button
            variant="danger"
            leftIcon={<Trash2 size={16} />}
            onClick={clearAll}
            loading={clearCache.isPending}
          >
            Cache tozalash
          </Button>
        }
      />

      <Card className={styles.summaryCard}>
        <CardHeader
          title="Cache holati"
          subtitle="Har 3 soatda avtomatik yangilanadi. So'nggi 50 yozuv ko'rsatilyapti."
          action={<Badge tone="accent" dot>Live</Badge>}
        />
        <div className={styles.summaryStats}>
          <div className={styles.summaryStat}>
            <div className={styles.summaryValue}>{snapshots.length}</div>
            <div className={styles.summaryLabel}>Jami snapshot</div>
          </div>
          <div className={styles.summaryStat}>
            <div className={styles.summaryValue}>
              {new Set(snapshots.map((s) => s.city)).size}
            </div>
            <div className={styles.summaryLabel}>Unikal shaharlar</div>
          </div>
          <div className={styles.summaryStat}>
            <div className={styles.summaryValue}>
              {snapshots[0]
                ? new Date(snapshots[0].fetched_at).toLocaleTimeString('uz-UZ', {
                    hour: '2-digit',
                    minute: '2-digit',
                  })
                : '—'}
            </div>
            <div className={styles.summaryLabel}>Oxirgi yangilanish</div>
          </div>
        </div>
      </Card>

      {isLoading ? (
        <div style={{ padding: '2rem', display: 'flex', justifyContent: 'center' }}>
          <Spinner size={24} />
        </div>
      ) : snapshots.length === 0 ? (
        <EmptyState
          icon={<Cloud size={20} />}
          title="Cache bo'sh"
          description="Foydalanuvchilar ob-havo so'ramagan yoki cache tozalangan"
        />
      ) : (
        <div className={styles.grid}>
          {snapshots.map((s) => {
            const Icon = iconFor(s.description);
            return (
              <Card key={s.id} className={styles.cityCard}>
                <div className={styles.cityHead}>
                  <div>
                    <div className={styles.cityName}>{s.city}</div>
                    <div className={styles.cityDesc}>{s.description}</div>
                  </div>
                  <Icon size={32} />
                </div>
                <div className={styles.temperature}>{Math.round(Number(s.temperature))}°C</div>
                <div className={styles.meta}>
                  <span>💧 {s.humidity}%</span>
                  <span className={styles.wind}>
                    <Wind size={12} /> his: {Math.round(Number(s.feels_like))}°
                  </span>
                </div>
                <div className={styles.cityFooter}>
                  <Badge tone="info">
                    <RefreshCw size={11} />
                    {new Date(s.fetched_at).toLocaleTimeString('uz-UZ', {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </Badge>
                  <span className={styles.timestamp}>
                    {new Date(s.fetched_at).toLocaleDateString('uz-UZ')}
                  </span>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </>
  );
}
