import { Users, UsersRound, ChefHat, CalendarDays, Bell } from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';

import { Card, CardHeader, PageHeader, Badge } from '@shared/ui';

import { StatCard } from './StatCard';
import styles from './DashboardPage.module.css';

/**
 * Boshqaruv paneli — birinchi tashrif sahifasi.
 *
 * ⚠️  Hozircha statistika demo data — backend'da tegishli endpoint
 * (`GET /admin/stats/` va h.k.) qo'shilganidan keyin `useQuery` bilan
 * to'ldiriladi.
 */
export function DashboardPage(): JSX.Element {
  return (
    <>
      <PageHeader
        title="Boshqaruv paneli"
        description="Menu Mate ekotizimining umumiy holati va so'nggi harakatlar"
      />

      <div className={styles.stats}>
        <StatCard label="Foydalanuvchilar" value={0} icon={Users} hint="Barcha ro'yxatdan o'tganlar" />
        <StatCard label="Oilalar" value={0} icon={UsersRound} hint="Faol oilalar" />
        <StatCard label="Retseptlar" value={35} icon={ChefHat} hint="Rasm bilan 100%" />
        <StatCard label="Aktiv menyular" value={0} icon={CalendarDays} hint="Bugungi holat" />
      </div>

      <div className={styles.grid}>
        <Card className={styles.chartCard}>
          <CardHeader
            title="Menyu yaratilishi (30 kun)"
            subtitle="Kunlik yangi menyular soni"
            action={<Badge tone="accent">Demo</Badge>}
          />
          <div className={styles.chartWrapper}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={demoChartData} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="accentFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--color-accent)" stopOpacity={0.45} />
                    <stop offset="100%" stopColor="var(--color-accent)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="var(--color-border-subtle)" strokeDasharray="4 4" />
                <XAxis
                  dataKey="day"
                  stroke="var(--color-text-muted)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={{ stroke: 'var(--color-border-subtle)' }}
                />
                <YAxis
                  stroke="var(--color-text-muted)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={{ stroke: 'var(--color-border-subtle)' }}
                  width={30}
                />
                <Tooltip
                  contentStyle={{
                    background: 'var(--color-bg-surface-2)',
                    border: '1px solid var(--color-border-default)',
                    borderRadius: '10px',
                    fontSize: '12px',
                  }}
                  labelStyle={{ color: 'var(--color-text-primary)' }}
                  itemStyle={{ color: 'var(--color-text-secondary)' }}
                />
                <Area
                  type="monotone"
                  dataKey="menus"
                  stroke="var(--color-accent)"
                  strokeWidth={2}
                  fill="url(#accentFill)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card>
          <CardHeader title="Tez amallar" subtitle="Ko'p ishlatiladigan sahifalar" />
          <div className={styles.quickList}>
            <QuickLink icon={<ChefHat size={16} />} label="Retseptni tahrirlash" />
            <QuickLink icon={<Bell size={16} />} label="Yangi bildirishnoma" />
            <QuickLink icon={<CalendarDays size={16} />} label="Bayram qo'shish" />
          </div>
        </Card>
      </div>
    </>
  );
}

function QuickLink({ icon, label }: { icon: React.ReactNode; label: string }): JSX.Element {
  return (
    <button className={styles.quickItem} disabled>
      <span className={styles.quickIcon}>{icon}</span>
      <span>{label}</span>
    </button>
  );
}

/** Vaqtinchalik grafik uchun demo ma'lumot (30 kun). */
const demoChartData = Array.from({ length: 30 }, (_, i) => ({
  day: `${i + 1}`,
  menus: Math.round(4 + Math.sin(i / 3) * 3 + Math.random() * 2),
}));
