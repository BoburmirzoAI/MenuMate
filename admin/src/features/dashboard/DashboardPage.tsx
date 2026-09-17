import { useNavigate } from 'react-router-dom';
import {
  Users,
  UsersRound,
  ChefHat,
  CalendarDays,
  Bell,
  ShoppingBasket,
  PartyPopper,
  Smartphone,
  Sprout,
  Shield,
  Cloud,
  ArrowRight,
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';

import { Card, CardHeader, PageHeader, Badge, Button } from '@shared/ui';
import { paths } from '@router/paths';

import { useDashboardStats } from './api';
import { StatCard } from './StatCard';
import styles from './DashboardPage.module.css';

/**
 * Boshqaruv paneli — real backend statistikasi va tez navigatsiya.
 *
 * KPI kartalar bosilganda tegishli sahifaga o'tadi.
 * Tez amallar tugmalari yordamida tez-tez ishlatiladigan sahifalar ochiladi.
 */
export function DashboardPage(): JSX.Element {
  const navigate = useNavigate();
  const { data, isLoading } = useDashboardStats();
  const kpi = data?.kpi;
  const chartData = data?.chart_menus_last_30_days ?? [];

  return (
    <>
      <PageHeader
        title="Boshqaruv paneli"
        description="Menu Mate ekotizimining umumiy holati va so'nggi harakatlar"
        actions={
          <>
            <Button
              variant="secondary"
              leftIcon={<Bell size={16} />}
              onClick={() => navigate(paths.notifications)}
            >
              Xabar yuborish
            </Button>
            <Button
              leftIcon={<ChefHat size={16} />}
              onClick={() => navigate(paths.recipes)}
            >
              Retseptlar
            </Button>
          </>
        }
      />

      <div className={styles.stats}>
        <StatCard
          label="Foydalanuvchilar"
          value={isLoading ? '…' : kpi?.total_users ?? 0}
          icon={Users}
          hint={`${kpi?.active_users ?? 0} faol`}
          onClick={() => navigate(paths.users)}
        />
        <StatCard
          label="Oilalar"
          value={isLoading ? '…' : kpi?.total_families ?? 0}
          icon={UsersRound}
          hint="Ro'yxatdan o'tgan oilalar"
          onClick={() => navigate(paths.families)}
        />
        <StatCard
          label="Retseptlar"
          value={isLoading ? '…' : kpi?.total_recipes ?? 0}
          icon={ChefHat}
          hint={`${kpi?.total_ingredients ?? 0} ingredient`}
          onClick={() => navigate(paths.recipes)}
        />
        <StatCard
          label="Aktiv menyular"
          value={isLoading ? '…' : kpi?.active_menus ?? 0}
          icon={CalendarDays}
          hint={`Oxirgi 30 kun: ${kpi?.menus_last_30_days ?? 0}`}
          onClick={() => navigate(paths.menus)}
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
            <QuickLink
              icon={<ChefHat size={16} />}
              label="Retseptlar"
              onClick={() => navigate(paths.recipes)}
            />
            <QuickLink
              icon={<Sprout size={16} />}
              label="Ingredientlar"
              onClick={() => navigate(paths.ingredients)}
            />
            <QuickLink
              icon={<Users size={16} />}
              label="Foydalanuvchilar"
              onClick={() => navigate(paths.users)}
            />
            <QuickLink
              icon={<UsersRound size={16} />}
              label="Oilalar"
              onClick={() => navigate(paths.families)}
            />
            <QuickLink
              icon={<Bell size={16} />}
              label="Xabar yuborish"
              onClick={() => navigate(paths.notifications)}
            />
            <QuickLink
              icon={<PartyPopper size={16} />}
              label="Bayramlar"
              onClick={() => navigate(paths.holidays)}
            />
          </div>
        </Card>
      </div>

      <div className={styles.grid}>
        <Card>
          <CardHeader
            title="Bildirishnomalar"
            subtitle="So'nggi holat"
            action={
              <Button
                variant="ghost"
                size="sm"
                rightIcon={<ArrowRight size={14} />}
                onClick={() => navigate(paths.notifications)}
              >
                Barchasi
              </Button>
            }
          />
          <div className={styles.miniList}>
            <MiniStat
              label="Jami xabarlar"
              value={kpi?.total_notifications ?? 0}
              tone="neutral"
            />
            <MiniStat
              label="O'qilmagan"
              value={kpi?.unread_notifications ?? 0}
              tone="warning"
            />
            <MiniStat
              label="Bayramlar"
              value={kpi?.total_holidays ?? 0}
              tone="accent"
            />
          </div>
        </Card>

        <Card>
          <CardHeader
            title="Qurilmalar"
            subtitle="FCM push va aktivlik"
            action={
              <Button
                variant="ghost"
                size="sm"
                rightIcon={<ArrowRight size={14} />}
                onClick={() => navigate(paths.devices)}
              >
                Ko'rish
              </Button>
            }
          />
          <div className={styles.miniList}>
            <MiniStat
              label="Jami qurilma"
              value={kpi?.total_devices ?? 0}
              tone="neutral"
              icon={<Smartphone size={14} />}
            />
            <MiniStat
              label="Push tokenli"
              value={kpi?.devices_with_fcm ?? 0}
              tone="success"
              icon={<Bell size={14} />}
            />
          </div>
        </Card>

        <Card>
          <CardHeader
            title="Tizim"
            subtitle="Boshqaruv"
            action={
              <Button
                variant="ghost"
                size="sm"
                rightIcon={<ArrowRight size={14} />}
                onClick={() => navigate(paths.permissions)}
              >
                Sozlash
              </Button>
            }
          />
          <div className={styles.systemList}>
            <SystemLink
              icon={<Shield size={16} />}
              label="Rollar va ruxsatlar"
              onClick={() => navigate(paths.permissions)}
            />
            <SystemLink
              icon={<Cloud size={16} />}
              label="Ob-havo cache"
              onClick={() => navigate(paths.weather)}
            />
            <SystemLink
              icon={<ShoppingBasket size={16} />}
              label="Xarid ro'yxatlari"
              onClick={() => navigate(paths.shopping)}
            />
          </div>
        </Card>
      </div>
    </>
  );
}

interface QuickLinkProps {
  icon: React.ReactNode;
  label: string;
  onClick: () => void;
}

function QuickLink({ icon, label, onClick }: QuickLinkProps): JSX.Element {
  return (
    <button className={styles.quickItem} onClick={onClick} type="button">
      <span className={styles.quickIcon}>{icon}</span>
      <span>{label}</span>
      <ArrowRight size={14} className={styles.quickArrow} />
    </button>
  );
}

interface MiniStatProps {
  label: string;
  value: number;
  tone: 'neutral' | 'success' | 'warning' | 'accent';
  icon?: React.ReactNode;
}

function MiniStat({ label, value, tone, icon }: MiniStatProps): JSX.Element {
  return (
    <div className={styles.miniStat}>
      <div className={styles.miniStatHead}>
        {icon && <span className={styles[`miniIcon-${tone}`]}>{icon}</span>}
        <span className={styles.miniLabel}>{label}</span>
      </div>
      <div className={styles.miniValue}>{value}</div>
    </div>
  );
}

interface SystemLinkProps {
  icon: React.ReactNode;
  label: string;
  onClick: () => void;
}

function SystemLink({ icon, label, onClick }: SystemLinkProps): JSX.Element {
  return (
    <button className={styles.systemItem} onClick={onClick} type="button">
      <span className={styles.quickIcon}>{icon}</span>
      <span>{label}</span>
      <ArrowRight size={14} className={styles.quickArrow} />
    </button>
  );
}
