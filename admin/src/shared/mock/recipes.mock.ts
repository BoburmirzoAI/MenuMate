import type { Recipe } from '@/types/domain';

/** DB da mavjud 35 retseptning namunali reprezentatsiyasi. */
export const mockRecipes: Recipe[] = [
  {
    id: 1, name: 'Osh (Palov)', name_uz: 'Osh (Palov)', name_ru: 'Плов', name_en: 'Pilaf',
    category: 'LUNCH', season: 'ANY', prep_time_minutes: 90, calories_per_serving: 620, servings: 4, is_hot: true,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Polu.jpg/330px-Polu.jpg',
    allergen_tags: [],
  },
  {
    id: 2, name: 'Manti', name_uz: 'Manti', name_ru: 'Манты', name_en: 'Manti',
    category: 'LUNCH', season: 'ANY', prep_time_minutes: 120, calories_per_serving: 480, servings: 4, is_hot: true,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Kayseride_bir_restoranda_Kayseri_mantı.jpg/330px-Kayseride_bir_restoranda_Kayseri_mantı.jpg',
    allergen_tags: [{ id: 1, name: 'Gluten', code: 'gluten', icon: '🌾' }],
  },
  {
    id: 3, name: 'Chuchvara', name_uz: 'Chuchvara', name_ru: 'Чучвара', name_en: 'Chuchvara',
    category: 'SOUP', season: 'WINTER', prep_time_minutes: 60, calories_per_serving: 350, servings: 4, is_hot: true,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Pelmeni_Russian.jpg/330px-Pelmeni_Russian.jpg',
    allergen_tags: [{ id: 1, name: 'Gluten', code: 'gluten', icon: '🌾' }],
  },
  {
    id: 4, name: 'Lag\'mon', name_uz: 'Lag\'mon', name_ru: 'Лагман', name_en: 'Lagman',
    category: 'LUNCH', season: 'ANY', prep_time_minutes: 75, calories_per_serving: 540, servings: 4, is_hot: true,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Порция_лагмана.jpg/330px-Порция_лагмана.jpg',
    allergen_tags: [{ id: 1, name: 'Gluten', code: 'gluten', icon: '🌾' }],
  },
  {
    id: 5, name: 'Sho\'rva', name_uz: 'Sho\'rva', name_ru: 'Шурпа', name_en: 'Shurpa',
    category: 'SOUP', season: 'WINTER', prep_time_minutes: 90, calories_per_serving: 380, servings: 4, is_hot: true,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Chorba_cooked_in_the_home_kitchen.jpg/330px-Chorba_cooked_in_the_home_kitchen.jpg',
    allergen_tags: [],
  },
  {
    id: 6, name: 'Somsa', name_uz: 'Somsa', name_ru: 'Самса', name_en: 'Samsa',
    category: 'LUNCH', season: 'ANY', prep_time_minutes: 60, calories_per_serving: 420, servings: 6, is_hot: true,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Chochure.jpg/330px-Chochure.jpg',
    allergen_tags: [{ id: 1, name: 'Gluten', code: 'gluten', icon: '🌾' }],
  },
  {
    id: 7, name: 'Non', name_uz: 'Non', name_ru: 'Лепёшка', name_en: 'Naan',
    category: 'BREAD', season: 'ANY', prep_time_minutes: 45, calories_per_serving: 250, servings: 4, is_hot: true,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Naan_in_Samarkand.jpg/330px-Naan_in_Samarkand.jpg',
    allergen_tags: [{ id: 1, name: 'Gluten', code: 'gluten', icon: '🌾' }],
  },
  {
    id: 8, name: 'Omlet', name_uz: 'Omlet', name_ru: 'Омлет', name_en: 'Omelette',
    category: 'BREAKFAST', season: 'ANY', prep_time_minutes: 15, calories_per_serving: 220, servings: 2, is_hot: true,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/FoodOmelete.jpg/330px-FoodOmelete.jpg',
    allergen_tags: [{ id: 2, name: 'Tuxum', code: 'egg', icon: '🥚' }],
  },
  {
    id: 9, name: 'Grekcha salat', name_uz: 'Grekcha salat', name_ru: 'Греческий салат', name_en: 'Greek salad',
    category: 'SALAD', season: 'SUMMER', prep_time_minutes: 15, calories_per_serving: 180, servings: 2, is_hot: false,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/GreekSalad.jpg/330px-GreekSalad.jpg',
    allergen_tags: [{ id: 3, name: 'Sut', code: 'dairy', icon: '🥛' }],
  },
  {
    id: 10, name: 'Ko\'k choy', name_uz: 'Ko\'k choy', name_ru: 'Зелёный чай', name_en: 'Green tea',
    category: 'DRINK', season: 'ANY', prep_time_minutes: 5, calories_per_serving: 5, servings: 1, is_hot: true,
    image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Tea_leaves_steeping_in_a_zhong_čaj_05.jpg/330px-Tea_leaves_steeping_in_a_zhong_čaj_05.jpg',
    allergen_tags: [],
  },
];
