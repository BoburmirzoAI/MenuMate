import { useState } from 'react';
import {
  Search,
  Clock,
  Flame,
  Snowflake,
  ChefHat,
  Plus,
  Pencil,
  Trash2,
} from 'lucide-react';

import {
  Badge,
  Button,
  Card,
  EmptyState,
  Input,
  Modal,
  PageHeader,
  Select,
  Spinner,
  toast,
} from '@shared/ui';
import type { Recipe, RecipeCategory } from '@/types/domain';

import { useRecipes, useDeleteRecipe } from './api';
import { RecipeFormModal } from './RecipeFormModal';
import styles from './RecipesPage.module.css';

const CATEGORY_LABELS: Record<RecipeCategory, string> = {
  BREAKFAST: 'Nonushta',
  LUNCH: 'Tushlik',
  DINNER: 'Kechki',
  SOUP: "Sho'rva",
  SALAD: 'Salat',
  DRINK: 'Ichimlik',
  BREAD: 'Non',
  DESSERT: 'Shirinlik',
};

/** Retseptlar boshqaruvi — grid + tafsilot modali. */
export function RecipesPage(): JSX.Element {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState<'all' | RecipeCategory>('all');
  const [selected, setSelected] = useState<Recipe | null>(null);
  const [formOpen, setFormOpen] = useState(false);
  const [editingRecipe, setEditingRecipe] = useState<Recipe | null>(null);

  const recipesParams: Parameters<typeof useRecipes>[0] = { search };
  if (category !== 'all') recipesParams.category = category;
  const { data: recipes = [], isLoading } = useRecipes(recipesParams);
  const deleteRecipe = useDeleteRecipe();

  const handleDelete = async (recipe: Recipe) => {
    if (!window.confirm(`"${recipe.name}" retseptini o'chirasizmi?`)) return;
    try {
      await deleteRecipe.mutateAsync(recipe.id);
      toast.info("Retsept o'chirildi", recipe.name);
      setSelected(null);
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : "O'chirilmadi");
    }
  };

  return (
    <>
      <PageHeader
        title="Retseptlar"
        description={
          isLoading ? 'Yuklanmoqda…' : `${recipes.length} retsept — 3 tilda (uz/ru/en) va rasm bilan`
        }
        actions={
          <Button
            leftIcon={<Plus size={16} />}
            onClick={() => {
              setEditingRecipe(null);
              setFormOpen(true);
            }}
          >
            Yangi retsept
          </Button>
        }
      />

      <Card padded={false} className={styles.filterCard}>
        <div className={styles.filters}>
          <Input
            placeholder="Retsept nomi bo'yicha qidirish..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            leftAdornment={<Search size={16} />}
          />
          <Select
            value={category}
            onChange={(e) => setCategory(e.target.value as 'all' | RecipeCategory)}
            options={[
              { label: 'Barcha kategoriyalar', value: 'all' },
              ...Object.entries(CATEGORY_LABELS).map(([value, label]) => ({
                label,
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
      ) : recipes.length === 0 ? (
        <EmptyState
          icon={<ChefHat size={20} />}
          title="Retsept topilmadi"
          description="Qidiruv yoki filterni o'zgartirib ko'ring"
        />
      ) : (
        <div className={styles.grid}>
          {recipes.map((recipe) => (
            <Card
              key={recipe.id}
              hoverable
              padded={false}
              onClick={() => setSelected(recipe)}
              className={styles.recipeCard}
            >
              <div
                className={styles.image}
                style={{ backgroundImage: `url(${recipe.image_url})` }}
              />
              <div className={styles.cardBody}>
                <div className={styles.cardHead}>
                  <Badge tone="accent">{CATEGORY_LABELS[recipe.category]}</Badge>
                  {recipe.is_hot ? (
                    <Badge tone="warning">
                      <Flame size={11} /> Issiq
                    </Badge>
                  ) : (
                    <Badge tone="info">
                      <Snowflake size={11} /> Salqin
                    </Badge>
                  )}
                </div>
                <div className={styles.recipeName}>{recipe.name}</div>
                <div className={styles.recipeMeta}>
                  <span className={styles.metaItem}>
                    <Clock size={12} />
                    {recipe.prep_time_minutes} daq.
                  </span>
                  <span className={styles.metaItem}>🔥 {recipe.calories_per_serving} kal</span>
                </div>
                {recipe.allergen_tags.length > 0 && (
                  <div className={styles.allergens}>
                    {recipe.allergen_tags.map((tag) => (
                      <span key={tag.id} className={styles.allergenTag}>
                        {tag.icon}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal
        open={selected !== null}
        onClose={() => setSelected(null)}
        title={selected?.name}
        size="lg"
        footer={
          selected && (
            <>
              <Button variant="ghost" onClick={() => setSelected(null)}>
                Yopish
              </Button>
              <Button
                variant="secondary"
                leftIcon={<Pencil size={16} />}
                onClick={() => {
                  setEditingRecipe(selected);
                  setSelected(null);
                  setFormOpen(true);
                }}
              >
                Tahrirlash
              </Button>
              <Button
                variant="danger"
                leftIcon={<Trash2 size={16} />}
                onClick={() => handleDelete(selected)}
              >
                O'chirish
              </Button>
            </>
          )
        }
      >
        {selected && (
          <div className={styles.modalContent}>
            <div
              className={styles.modalImage}
              style={{ backgroundImage: `url(${selected.image_url})` }}
            />
            <div className={styles.modalGrid}>
              <ModalStat label="Kategoriya" value={CATEGORY_LABELS[selected.category]} />
              <ModalStat label="Vaqt" value={`${selected.prep_time_minutes} daq.`} />
              <ModalStat label="Kaloriya" value={`${selected.calories_per_serving} kal`} />
              <ModalStat label="Porsiya" value={`${selected.servings} kishi`} />
              <ModalStat label="Mavsum" value={selected.season} />
              <ModalStat label="Harorat" value={selected.is_hot ? 'Issiq' : 'Salqin'} />
            </div>

            <div className={styles.namesBlock}>
              <div className={styles.namesLabel}>Nomi (3 tilda)</div>
              <div className={styles.namesGrid}>
                <div>🇺🇿 <strong>{selected.name_uz}</strong></div>
                <div>🇷🇺 <strong>{selected.name_ru}</strong></div>
                <div>🇬🇧 <strong>{selected.name_en}</strong></div>
              </div>
            </div>

            {selected.allergen_tags.length > 0 && (
              <div className={styles.allergenBlock}>
                <div className={styles.namesLabel}>Allergenlar</div>
                <div className={styles.allergenList}>
                  {selected.allergen_tags.map((tag) => (
                    <Badge key={tag.id} tone="warning">
                      {tag.icon} {tag.name}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>

      <RecipeFormModal
        open={formOpen}
        onClose={() => setFormOpen(false)}
        recipe={editingRecipe}
      />
    </>
  );
}

function ModalStat({ label, value }: { label: string; value: string }): JSX.Element {
  return (
    <div className={styles.statBlock}>
      <div className={styles.statLabel}>{label}</div>
      <div className={styles.statValue}>{value}</div>
    </div>
  );
}
