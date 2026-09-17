import { useMemo, useState } from 'react';
import { Search, Sprout } from 'lucide-react';

import { Card, EmptyState, Input, PageHeader, Select, Spinner } from '@shared/ui';
import type { Ingredient } from '@/types/domain';

import { useIngredients } from '@features/recipes/api';
import styles from './IngredientsPage.module.css';

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

/** Ingredientlar boshqaruvi — rasm + kategoriya bo'yicha guruh. */
export function IngredientsPage(): JSX.Element {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState<string>('all');

  const ingredientParams: Parameters<typeof useIngredients>[0] = { search };
  if (category !== 'all') ingredientParams.category = category;
  const { data: ingredients = [], isLoading } = useIngredients(ingredientParams);

  const grouped = useMemo(() => {
    const groups: Record<string, Ingredient[]> = {};
    for (const ing of ingredients) {
      if (!groups[ing.category]) groups[ing.category] = [];
      groups[ing.category]!.push(ing);
    }
    return groups;
  }, [ingredients]);

  return (
    <>
      <PageHeader
        title="Ingredientlar"
        description={
          isLoading
            ? 'Yuklanmoqda…'
            : `${ingredients.length} ingredient — kategoriya bo'yicha guruhlangan, avtomatik rasm bilan`
        }
      />

      <Card padded={false} className={styles.filterCard}>
        <div className={styles.filters}>
          <Input
            placeholder="Ingredient qidirish..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            leftAdornment={<Search size={16} />}
          />
          <Select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            options={[
              { label: 'Barcha kategoriyalar', value: 'all' },
              ...Object.entries(CATEGORY_LABELS).map(([value, { label, icon }]) => ({
                label: `${icon} ${label}`,
                value,
              })),
            ]}
          />
        </div>
      </Card>

      {isLoading ? (
        <div style={{ padding: '2rem', display: 'flex', justifyContent: 'center' }}>
          <Spinner size={24} />
        </div>
      ) : Object.keys(grouped).length === 0 ? (
        <EmptyState
          icon={<Sprout size={20} />}
          title="Ingredient topilmadi"
          description="Filterni o'zgartirib ko'ring"
        />
      ) : (
        <div className={styles.groups}>
          {Object.entries(grouped).map(([cat, items]) => {
            const meta = CATEGORY_LABELS[cat] ?? { label: cat, icon: '📦' };
            return (
              <div key={cat} className={styles.group}>
                <div className={styles.groupHeader}>
                  <span className={styles.groupIcon}>{meta.icon}</span>
                  <span className={styles.groupLabel}>{meta.label}</span>
                  <span className={styles.groupCount}>{items.length}</span>
                </div>
                <div className={styles.grid}>
                  {items.map((ing) => (
                    <div key={ing.id} className={styles.ingCard}>
                      <div
                        className={styles.ingImage}
                        style={{ backgroundImage: `url(${ing.image_url})` }}
                      />
                      <div className={styles.ingName}>{ing.name}</div>
                      <div className={styles.ingUnit}>{ing.unit}</div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </>
  );
}
