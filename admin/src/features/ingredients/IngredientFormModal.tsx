import { useEffect, useState } from 'react';
import { Plus, Pencil, Sprout } from 'lucide-react';

import { Button, Input, Modal, Select, toast } from '@shared/ui';
import type { Ingredient } from '@/types/domain';

import {
  useCreateIngredient,
  useUpdateIngredient,
  type IngredientPayload,
} from '@features/recipes/api';
import styles from './IngredientFormModal.module.css';

interface IngredientFormModalProps {
  open: boolean;
  onClose: () => void;
  ingredient: Ingredient | null;
}

interface FormState {
  name_uz: string;
  name_ru: string;
  name_en: string;
  category: string;
  default_unit: string;
  image_url: string;
}

const initialState: FormState = {
  name_uz: '',
  name_ru: '',
  name_en: '',
  category: 'VEGETABLE',
  default_unit: 'g',
  image_url: '',
};

const CATEGORY_OPTIONS = [
  { label: '🥬 Sabzavot', value: 'VEGETABLE' },
  { label: '🍎 Meva', value: 'FRUIT' },
  { label: '🥩 Go\'sht', value: 'MEAT' },
  { label: '🥛 Sut mahsuloti', value: 'DAIRY' },
  { label: '🌾 Don mahsuloti', value: 'GRAIN' },
  { label: '🌶️ Ziravor', value: 'SPICE' },
  { label: '🫒 Yog\'', value: 'OIL' },
  { label: '📦 Boshqa', value: 'OTHER' },
];

const UNIT_OPTIONS = [
  { label: 'gramm (g)', value: 'g' },
  { label: 'kilogramm (kg)', value: 'kg' },
  { label: 'litr (l)', value: 'l' },
  { label: 'millilitr (ml)', value: 'ml' },
  { label: 'dona (pcs)', value: 'pcs' },
  { label: 'choy qoshiq (tsp)', value: 'tsp' },
  { label: 'osh qoshiq (tbsp)', value: 'tbsp' },
];

/** Ingredient CRUD modal — 3 tilli nom + kategoriya + birlik. */
export function IngredientFormModal({
  open,
  onClose,
  ingredient,
}: IngredientFormModalProps): JSX.Element {
  const isEdit = ingredient !== null;
  const [form, setForm] = useState<FormState>(initialState);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const createIngredient = useCreateIngredient();
  const updateIngredient = useUpdateIngredient();

  useEffect(() => {
    if (!open) return;
    if (ingredient) {
      setForm({
        name_uz: ingredient.name_uz ?? '',
        name_ru: ingredient.name_ru ?? '',
        name_en: ingredient.name_en ?? '',
        category: ingredient.category,
        default_unit: ingredient.unit,
        image_url: ingredient.image_url ?? '',
      });
    } else {
      setForm(initialState);
    }
    setErrors({});
  }, [open, ingredient]);

  const update = <K extends keyof FormState>(key: K, value: FormState[K]) => {
    setForm((f) => ({ ...f, [key]: value }));
    setErrors((e) => ({ ...e, [key]: '' }));
  };

  const handleSubmit = async () => {
    const errs: Record<string, string> = {};
    if (!form.name_uz.trim()) errs.name_uz = "O'zbekcha nom kerak";
    if (!form.name_ru.trim()) errs.name_ru = 'Ruscha nom kerak';
    if (!form.name_en.trim()) errs.name_en = 'Inglizcha nom kerak';
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;

    const payload: IngredientPayload = {
      name_uz: form.name_uz,
      name_ru: form.name_ru,
      name_en: form.name_en,
      category: form.category,
      default_unit: form.default_unit,
      image_url: form.image_url,
    };

    try {
      if (isEdit && ingredient) {
        await updateIngredient.mutateAsync({ id: ingredient.id, ...payload });
        toast.success('Ingredient yangilandi', form.name_uz);
      } else {
        await createIngredient.mutateAsync(payload);
        toast.success("Yangi ingredient qo'shildi", form.name_uz);
      }
      onClose();
    } catch (err) {
      toast.error('Xatolik', err instanceof Error ? err.message : 'Bajarilmadi');
    }
  };

  const submitting = createIngredient.isPending || updateIngredient.isPending;

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={
        <span className={styles.title}>
          {isEdit ? <Pencil size={16} /> : <Plus size={16} />}
          {isEdit ? 'Ingredientni tahrirlash' : 'Yangi ingredient'}
        </span>
      }
      size="md"
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
          <div className={styles.sectionTitle}>Nom (3 tilda)</div>
          <div className={styles.namesGrid}>
            <Input
              label="🇺🇿 O'zbekcha *"
              value={form.name_uz}
              onChange={(e) => update('name_uz', e.target.value)}
              placeholder="Sabzi"
              leftAdornment={<Sprout size={14} />}
              {...(errors.name_uz ? { errorText: errors.name_uz } : {})}
            />
            <Input
              label="🇷🇺 Русский *"
              value={form.name_ru}
              onChange={(e) => update('name_ru', e.target.value)}
              placeholder="Морковь"
              {...(errors.name_ru ? { errorText: errors.name_ru } : {})}
            />
            <Input
              label="🇬🇧 English *"
              value={form.name_en}
              onChange={(e) => update('name_en', e.target.value)}
              placeholder="Carrot"
              {...(errors.name_en ? { errorText: errors.name_en } : {})}
            />
          </div>
        </div>

        <div className={styles.section}>
          <div className={styles.sectionTitle}>Turkum va birlik</div>
          <div className={styles.row}>
            <Select
              label="Kategoriya"
              value={form.category}
              onChange={(e) => update('category', e.target.value)}
              options={CATEGORY_OPTIONS}
            />
            <Select
              label="Birlik"
              value={form.default_unit}
              onChange={(e) => update('default_unit', e.target.value)}
              options={UNIT_OPTIONS}
            />
          </div>
          <Input
            label="Rasm URL (ixtiyoriy)"
            value={form.image_url}
            onChange={(e) => update('image_url', e.target.value)}
            placeholder="https://... (bo'sh bo'lsa Wikipedia'dan)"
            hint="Bo'sh qoldirsangiz Wikipedia yoki Karzinka'dan dinamik olinadi"
          />
        </div>
      </div>
    </Modal>
  );
}
