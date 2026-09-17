import { useMemo, useState, useEffect } from 'react';
import { ShoppingBasket, CheckCircle2 } from 'lucide-react';

import { Badge, Card, EmptyState, PageHeader, Select, Spinner } from '@shared/ui';

import { useMenus } from '@features/menus/api';
import { useShoppingByMenu, type ShoppingItemAdmin } from './api';
import styles from './ShoppingPage.module.css';

const CATEGORY_LABELS: Record<string, { label: string; icon: string }> = {
  DAIRY: { label: 'Sut mahsulotlari', icon: '🥛' },
  MEAT: { label: "Go'sht", icon: '🥩' },
  FRUIT: { label: 'Meva', icon: '🍎' },
  VEGETABLE: { label: 'Sabzavot', icon: '🥬' },
  GRAIN: { label: 'Don', icon: '🌾' },
  SPICE: { label: 'Ziravor', icon: '🌶️' },
  OIL: { label: "Yog'", icon: '🫒' },
  OTHER: { label: 'Boshqa', icon: '📦' },
};

/** Xarid ro'yxatlari sahifasi — menyu tanlanadi va shu menyu uchun list ko'rsatiladi. */
export function ShoppingPage(): JSX.Element {
  const { data: menus = [], isLoading: menusLoading } = useMenus();
  const [selectedMenuId, setSelectedMenuId] = useState<number | null>(null);

  // Menyular kelgach — birinchisini tanlaymiz
  useEffect(() => {
    if (menus.length > 0 && selectedMenuId === null) {
      setSelectedMenuId(menus[0]!.id);
    }
  }, [menus, selectedMenuId]);

  const { data: shoppingList, isLoading: listLoading } = useShoppingByMenu(selectedMenuId);
  const items: ShoppingItemAdmin[] = shoppingList?.items ?? [];
  const currentMenu = menus.find((m) => m.id === selectedMenuId) ?? null;

  const purchasedCount = items.filter((i) => i.is_purchased).length;
  const progress = items.length > 0 ? Math.round((purchasedCount / items.length) * 100) : 0;

  const grouped = useMemo(() => {
    const groups: Record<string, ShoppingItemAdmin[]> = {};
    for (const item of items) {
      if (!groups[item.category]) groups[item.category] = [];
      groups[item.category]!.push(item);
    }
    return groups;
  }, [items]);

  return (
    <>
      <PageHeader
        title="Xarid ro'yxatlari"
        description="Har menyu uchun avtomatik tuzilgan mahsulot ro'yxati"
      />

      <div className={styles.header}>
        <Card padded={false} className={styles.selectorCard}>
          <div className={styles.selectorLabel}>Menyu tanlang</div>
          <Select
            value={selectedMenuId != null ? String(selectedMenuId) : ''}
            onChange={(e) => setSelectedMenuId(Number(e.target.value))}
            options={menus.map((m) => ({
              label: `#${m.id} · ${m.family_name || 'Oila'} · ${new Date(m.start_date).toLocaleDateString('uz-UZ')}`,
              value: String(m.id),
            }))}
            placeholder={menusLoading ? 'Yuklanmoqda…' : 'Menyu tanlang'}
          />
        </Card>

        <Card className={styles.progressCard}>
          <div className={styles.progressStats}>
            <CheckCircle2 size={20} className={styles.progressIcon} />
            <div>
              <div className={styles.progressValue}>
                {purchasedCount} / {items.length}
              </div>
              <div className={styles.progressLabel}>sotib olindi ({progress}%)</div>
            </div>
          </div>
          <div className={styles.progressBar}>
            <div className={styles.progressFill} style={{ width: `${progress}%` }} />
          </div>
        </Card>
      </div>

      {currentMenu && (
        <div className={styles.familyInfo}>
          <Badge tone="accent">{currentMenu.family_name}</Badge>
          <Badge tone="warning">
            {new Date(currentMenu.start_date).toLocaleDateString('uz-UZ')} —{' '}
            {new Date(currentMenu.end_date).toLocaleDateString('uz-UZ')}
          </Badge>
        </div>
      )}

      {listLoading ? (
        <div style={{ padding: '2rem', display: 'flex', justifyContent: 'center' }}>
          <Spinner size={24} />
        </div>
      ) : items.length === 0 ? (
        <EmptyState
          icon={<ShoppingBasket size={20} />}
          title="Xarid ro'yxati bo'sh"
          description="Bu menyu uchun mahsulotlar hisoblanmagan"
        />
      ) : (
      <div className={styles.groups}>
        {Object.entries(grouped).map(([cat, catItems]) => {
          const meta = CATEGORY_LABELS[cat] ?? { label: cat, icon: '📦' };
          return (
            <div key={cat} className={styles.group}>
              <div className={styles.groupHeader}>
                <span className={styles.groupIcon}>{meta.icon}</span>
                <span className={styles.groupLabel}>{meta.label}</span>
                <span className={styles.groupCount}>{catItems.length}</span>
              </div>
              {catItems.map((item) => (
                <div
                  key={item.ingredient_id}
                  className={`${styles.item} ${item.is_purchased ? styles.itemPurchased : ''}`}
                >
                  <ShoppingBasket
                    size={16}
                    className={item.is_purchased ? styles.iconDone : styles.iconPending}
                  />
                  <div className={styles.itemName}>{item.ingredient_name}</div>
                  <div className={styles.itemAmount}>
                    {item.total_amount} {item.unit}
                  </div>
                </div>
              ))}
            </div>
          );
        })}
      </div>
      )}
    </>
  );
}
