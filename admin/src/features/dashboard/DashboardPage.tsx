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

import { useDashboardStats } from './api';
import { StatCard } from './StatCard';
import styles from './DashboardPage.module.css';

/** Boshqaruv paneli — real backend statistikasi. */
export function DashboardPage(): JSX.Element {
  const { data, isLoading } = useDashboardStats();
  const kpi = data?.kpi;
  const chartData = data?.chart_menus_last_30_days ?? [];

  return (
    <>
      <PageHeader
        title="Boshqaruv paneli"
        description="Menu Mate ekotizimining umumiy holati va so'nggi harakatlar"
      />

      <div className={styles.stats}>
        <StatCard
          label="Foydalanuvchilar"
          value={isLoading ? '…' : kpi?.total_users ?? 0}
          icon={Users}
          hint={`${kpi?.active_users ?? 0} faol`}
        />
        <StatCard
          label="Oilalar"
          value={isLoading ? '…' : kpi?.total_families ?? 0}
          icon={UsersRound}
          hint="Ro'yxatdan o'tgan oilalar"
        />
        <StatCard
          label="Retseptlar"
          value={isLoading ? '…' : kpi?.total_recipes ?? 0}
          icon={ChefHat}
          hint={`${kpi?.total_ingredients ?? 0} ingredient`}
        />
        <StatCard
          label="Aktiv menyular"
          value={isLoading ? '…' : kpi?.active_menus ?? 0}
          icon={CalendarDays}
          hint={`Oxirgi 30 kun: ${kpi?.menus_last_30_days ?? 0}`}
        />
      </div>

      <div className={styles.grid}>
        <Card className={styles.chartCard}>
          <CardHeader
            title="Menyu yaratilishi (30 kun)"
            subtitle="Kunlik yangi menyular soni"
            action={<Badge tone="accent">Live</Badge>}
          />
          <div className={styles.chartWrapper}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
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
