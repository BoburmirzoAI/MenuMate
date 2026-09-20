import { useEffect, useState } from 'react';
import { Plus, Pencil, Flame, Snowflake } from 'lucide-react';

import {
  Button,
  Checkbox,
  Input,
  Modal,
  Select,
  toast,
} from '@shared/ui';
import type { Recipe } from '@/types/domain';

import {
  useCreateRecipe,
  useUpdateRecipe,
  useAllergens,
  type RecipePayload,
} from './api';
import { RecipeImagePicker } from './RecipeImagePicker';
import styles from './RecipeFormModal.module.css';

interface RecipeFormModalProps {
  open: boolean;
  onClose: () => void;
  recipe: Recipe | null;
}

interface FormState {
  name_uz: string;
  name_ru: string;
  name_en: string;
  description_uz: string;
  description_ru: string;
  description_en: string;
  category: string;
  season: string;
  prep_time_minutes: number;
  calories_per_serving: number;
  servings: number;
  is_hot: boolean;
  image_url: string;
  allergen_ids: number[];
}

const initialState: FormState = {
  name_uz: '',
  name_ru: '',
  name_en: '',
  description_uz: '',
  description_ru: '',
  description_en: '',
  category: 'LUNCH',
  season: 'ALL',
  prep_time_minutes: 30,
  calories_per_serving: 400,
  servings: 4,
  is_hot: true,
  image_url: '',
  allergen_ids: [],
};

const CATEGORY_OPTIONS = [
  { label: 'Nonushta', value: 'BREAKFAST' },
  { label: 'Tushlik', value: 'LUNCH' },
  { label: 'Kechki ovqat', value: 'DINNER' },
  { label: 'Salat', value: 'SALAD' },
  { label: "Sho'rva", value: 'SOUP' },
  { label: 'Ichimlik', value: 'DRINK' },
  { label: 'Shirinlik', value: 'DESSERT' },
  { label: 'Non mahsuloti', value: 'BREAD' },
  { label: 'Yengil taom', value: 'SNACK' },
];

const SEASON_OPTIONS = [
  { label: 'Har doim', value: 'ALL' },
  { label: 'Yoz', value: 'SUMMER' },
  { label: 'Qish', value: 'WINTER' },
  { label: 'Bahor', value: 'SPRING' },
  { label: 'Kuz', value: 'AUTUMN' },
];

/** Retsept CRUD modal — 3 tilli nom + tavsif + kategoriya + allergen. */
export function RecipeFormModal({
  open,
  onClose,
  recipe,
}: RecipeFormModalProps): JSX.Element {
  const isEdit = recipe !== null;
  const [form, setForm] = useState<FormState>(initialState);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const createRecipe = useCreateRecipe();
  const updateRecipe = useUpdateRecipe();
  const { data: allergens = [] } = useAllergens();

  useEffect(() => {
    if (!open) return;
    if (recipe) {
      setForm({
        name_uz: recipe.name_uz ?? '',
        name_ru: recipe.name_ru ?? '',
        name_en: recipe.name_en ?? '',
        description_uz: '',
        description_ru: '',
        description_en: '',
        category: recipe.category,
        season: recipe.season,
        prep_time_minutes: recipe.prep_time_minutes,
        calories_per_serving: recipe.calories_per_serving,
        servings: recipe.servings,
        is_hot: recipe.is_hot,
        image_url: recipe.image_url ?? '',
        allergen_ids: recipe.allergen_tags.map((t) => t.id),
      });
    } else {
      setForm(initialState);
    }
    setErrors({});
  }, [open, recipe]);

  const update = <K extends keyof FormState>(key: K, value: FormState[K]) => {
    setForm((f) => ({ ...f, [key]: value }));
    setErrors((e) => ({ ...e, [key]: '' }));
  };

  const toggleAllergen = (id: number) => {
    setForm((f) => ({
      ...f,
      allergen_ids: f.allergen_ids.includes(id)
        ? f.allergen_ids.filter((x) => x !== id)
        : [...f.allergen_ids, id],
    }));
  };

  const handleSubmit = async () => {
    const errs: Record<string, string> = {};
    if (!form.name_uz.trim()) errs.name_uz = "O'zbekcha nom kerak";
    if (!form.name_ru.trim()) errs.name_ru = 'Ruscha nom kerak';
    if (!form.name_en.trim()) errs.name_en = 'Inglizcha nom kerak';
    if (form.prep_time_minutes <= 0) errs.prep_time_minutes = 'Vaqt musbat bo\'lishi kerak';
    if (form.calories_per_serving <= 0) errs.calories_per_serving = 'Musbat son';
    if (form.servings <= 0) errs.servings = 'Musbat son';
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;

    const payload: RecipePayload = {
      name_uz: form.name_uz,
      name_ru: form.name_ru,
      name_en: form.name_en,
      description_uz: form.description_uz,
      description_ru: form.description_ru,
      description_en: form.description_en,
      category: form.category,
      season: form.season,
      prep_time_minutes: form.prep_time_minutes,
      calories_per_serving: form.calories_per_serving,
      servings: form.servings,
      is_hot: form.is_hot,
      image_url: form.image_url,
      allergen_tag_ids: form.allergen_ids,
    };

    try {
      if (isEdit && recipe) {
        await updateRecipe.mutateAsync({ id: recipe.id, ...payload });
        toast.success('Retsept yangilandi', form.name_uz);
      } else {
        await createRecipe.mutateAsync(payload);
        toast.success("Yangi retsept qo'shildi", form.name_uz);
      }
      onClose();
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Bajarilmadi');
    }
  };

  const submitting = createRecipe.isPending || updateRecipe.isPending;

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={
        <span className={styles.title}>
          {isEdit ? <Pencil size={16} /> : <Plus size={16} />}
          {isEdit ? 'Retseptni tahrirlash' : 'Yangi retsept'}
        </span>
      }
      size="lg"
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Bekor
          </Button>
          <Button onClick={handleSubmit} loading={submitting}>
            {isEdit ? 'Saqlash' : "Qo'shish"}
          </Button>
        </>
      }
    >
      <div className={styles.form}>
        <div className={styles.section}>
          <div className={styles.sectionTitle}>Nom (3 tilda majburiy)</div>
          <div className={styles.namesRow}>
            <Input
              label="🇺🇿 O'zbekcha *"
              value={form.name_uz}
              onChange={(e) => update('name_uz', e.target.value)}
              {...(errors.name_uz ? { errorText: errors.name_uz } : {})}
            />
            <Input
              label="🇷🇺 Русский *"
              value={form.name_ru}
              onChange={(e) => update('name_ru', e.target.value)}
              {...(errors.name_ru ? { errorText: errors.name_ru } : {})}
            />
            <Input
              label="🇬🇧 English *"
              value={form.name_en}
              onChange={(e) => update('name_en', e.target.value)}
              {...(errors.name_en ? { errorText: errors.name_en } : {})}
            />
          </div>
        </div>

        <div className={styles.section}>
          <div className={styles.sectionTitle}>Asosiy ma'lumotlar</div>
          <div className={styles.row}>
            <Select
              label="Kategoriya"
              value={form.category}
              onChange={(e) => update('category', e.target.value)}
              options={CATEGORY_OPTIONS}
            />
            <Select
              label="Mavsum"
              value={form.season}
              onChange={(e) => update('season', e.target.value)}
              options={SEASON_OPTIONS}
            />
          </div>
          <div className={styles.row3}>
            <Input
              label="Vaqt (daq.)"
              type="number"
              min={1}
              value={form.prep_time_minutes}
              onChange={(e) => update('prep_time_minutes', Number(e.target.value))}
              {...(errors.prep_time_minutes
                ? { errorText: errors.prep_time_minutes }
                : {})}
            />
            <Input
              label="Kaloriya"
              type="number"
              min={1}
              value={form.calories_per_serving}
              onChange={(e) => update('calories_per_serving', Number(e.target.value))}
              {...(errors.calories_per_serving
                ? { errorText: errors.calories_per_serving }
                : {})}
            />
            <Input
              label="Porsiya"
              type="number"
              min={1}
              value={form.servings}
              onChange={(e) => update('servings', Number(e.target.value))}
              {...(errors.servings ? { errorText: errors.servings } : {})}
            />
          </div>
          <div className={styles.imageSection}>
            <div className={styles.sectionLabel}>Rasm</div>
            <RecipeImagePicker
              value={form.image_url}
              onChange={(url) => update('image_url', url)}
              query={form.name_uz || form.name_en || form.name_ru}
            />
          </div>
          <div className={styles.row}>
            <div className={styles.hotToggle}>
              <div className={styles.toggleLabel}>Harorat</div>
              <div className={styles.toggleRow}>
                <button
                  className={`${styles.toggleBtn} ${form.is_hot ? styles.toggleActive : ''}`}
                  onClick={() => update('is_hot', true)}
                  type="button"
                >
                  <Flame size={14} /> Issiq
                </button>
                <button
                  className={`${styles.toggleBtn} ${!form.is_hot ? styles.toggleActive : ''}`}
                  onClick={() => update('is_hot', false)}
                  type="button"
                >
                  <Snowflake size={14} /> Salqin
                </button>
              </div>
            </div>
          </div>
        </div>

        {allergens.length > 0 && (
          <div className={styles.section}>
            <div className={styles.sectionTitle}>Allergenlar</div>
            <div className={styles.allergenGrid}>
              {allergens.map((tag) => (
                <label
                  key={tag.id}
                  className={`${styles.allergenChip} ${form.allergen_ids.includes(tag.id) ? styles.allergenActive : ''}`}
                >
                  <Checkbox
                    checked={form.allergen_ids.includes(tag.id)}
                    onChange={() => toggleAllergen(tag.id)}
                  />
                  <span>{tag.name}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        <div className={styles.section}>
          <div className={styles.sectionTitle}>Tavsif (ixtiyoriy)</div>
          <textarea
            className={styles.textarea}
            rows={2}
            placeholder="🇺🇿 O'zbekcha tavsif..."
            value={form.description_uz}
            onChange={(e) => update('description_uz', e.target.value)}
          />
          <textarea
            className={styles.textarea}
            rows={2}
            placeholder="🇷🇺 Русское описание..."
            value={form.description_ru}
            onChange={(e) => update('description_ru', e.target.value)}
          />
          <textarea
            className={styles.textarea}
            rows={2}
            placeholder="🇬🇧 English description..."
            value={form.description_en}
            onChange={(e) => update('description_en', e.target.value)}
          />
        </div>
      </div>
    </Modal>
  );
}
