/// Sodda i18n — kalit → 3 tildagi qiymatlar.
class AppStrings {
  AppStrings._();

  static const Map<String, Map<String, String>> _strings = {
    // ========================================================================
    // Umumiy (common)
    // ========================================================================
    'app_name': {'uz': 'Menu Mate', 'ru': 'Menu Mate', 'en': 'Menu Mate'},
    'loading': {'uz': 'Yuklanmoqda...', 'ru': 'Загрузка...', 'en': 'Loading...'},
    'error': {'uz': 'Xatolik', 'ru': 'Ошибка', 'en': 'Error'},
    'retry': {'uz': 'Qayta urinish', 'ru': 'Повторить', 'en': 'Retry'},
    'cancel': {'uz': 'Bekor', 'ru': 'Отмена', 'en': 'Cancel'},
    'save': {'uz': 'Saqlash', 'ru': 'Сохранить', 'en': 'Save'},
    'delete': {'uz': "O'chirish", 'ru': 'Удалить', 'en': 'Delete'},
    'confirm': {'uz': 'Tasdiqlash', 'ru': 'Подтвердить', 'en': 'Confirm'},
    'next': {'uz': 'Keyingi', 'ru': 'Далее', 'en': 'Next'},
    'back': {'uz': 'Orqaga', 'ru': 'Назад', 'en': 'Back'},
    'skip': {'uz': "O'tkazib yuborish", 'ru': 'Пропустить', 'en': 'Skip'},
    'done': {'uz': 'Tayyor', 'ru': 'Готово', 'en': 'Done'},
    'add': {'uz': "Qo'shish", 'ru': 'Добавить', 'en': 'Add'},
    'edit': {'uz': 'Tahrirlash', 'ru': 'Редактировать', 'en': 'Edit'},
    'close': {'uz': 'Yopish', 'ru': 'Закрыть', 'en': 'Close'},
    'open': {'uz': 'Ochish', 'ru': 'Открыть', 'en': 'Open'},
    'copy': {'uz': 'Nusxa', 'ru': 'Копия', 'en': 'Copy'},
    'copied': {'uz': "Nusxa olindi", 'ru': 'Скопировано', 'en': 'Copied'},
    'search': {'uz': 'Qidirish', 'ru': 'Поиск', 'en': 'Search'},
    'select': {'uz': 'Tanlash', 'ru': 'Выбрать', 'en': 'Select'},
    'all': {'uz': 'Barchasi', 'ru': 'Все', 'en': 'All'},
    'yes': {'uz': 'Ha', 'ru': 'Да', 'en': 'Yes'},
    'no': {'uz': "Yo'q", 'ru': 'Нет', 'en': 'No'},
    'hello': {'uz': 'Assalomu alaykum', 'ru': 'Здравствуйте', 'en': 'Hello'},
    'not_selected': {'uz': 'Tanlanmagan', 'ru': 'Не выбрано', 'en': 'Not selected'},
    'not_found': {'uz': 'Topilmadi', 'ru': 'Не найдено', 'en': 'Not found'},
    'coming_soon': {'uz': 'Tez orada', 'ru': 'Скоро', 'en': 'Coming soon'},
    'user': {'uz': 'Foydalanuvchi', 'ru': 'Пользователь', 'en': 'User'},

    // Vaqt oralig'i
    'time_just_now': {'uz': 'Hozirgina', 'ru': 'Только что', 'en': 'Just now'},
    'time_min_ago': {'uz': 'daq oldin', 'ru': 'мин назад', 'en': 'min ago'},
    'time_hour_ago': {'uz': 'soat oldin', 'ru': 'ч назад', 'en': 'hr ago'},
    'time_day_ago': {'uz': 'kun oldin', 'ru': 'дн назад', 'en': 'd ago'},

    // ========================================================================
    // Nav
    // ========================================================================
    'nav_home': {'uz': 'Bosh', 'ru': 'Главная', 'en': 'Home'},
    'nav_menu': {'uz': 'Menyu', 'ru': 'Меню', 'en': 'Menu'},
    'nav_shopping': {'uz': 'Xarid', 'ru': 'Покупки', 'en': 'Shopping'},
    'nav_recipes': {'uz': 'Retsept', 'ru': 'Рецепты', 'en': 'Recipes'},
    'nav_profile': {'uz': 'Profil', 'ru': 'Профиль', 'en': 'Profile'},

    // ========================================================================
    // Auth
    // ========================================================================
    'login': {'uz': 'Kirish', 'ru': 'Войти', 'en': 'Sign In'},
    'register': {'uz': "Ro'yxatdan o'tish", 'ru': 'Регистрация', 'en': 'Sign Up'},
    'logout': {'uz': 'Chiqish', 'ru': 'Выйти', 'en': 'Sign Out'},
    'email': {'uz': 'Email', 'ru': 'Email', 'en': 'Email'},
    'password': {'uz': 'Parol', 'ru': 'Пароль', 'en': 'Password'},
    'password_confirm': {'uz': 'Parolni takrorlang', 'ru': 'Повторите пароль', 'en': 'Confirm password'},
    'first_name': {'uz': 'Ism', 'ru': 'Имя', 'en': 'First name'},
    'last_name': {'uz': 'Familiya', 'ru': 'Фамилия', 'en': 'Last name'},
    'forgot_password': {'uz': 'Parolni unutdim', 'ru': 'Забыли пароль?', 'en': 'Forgot password?'},
    'forgot_password_hint': {
      'uz': "Email manzilingizni kiriting — tiklash kodini yuboramiz.",
      'ru': 'Введите email — отправим код восстановления.',
      'en': 'Enter your email — we will send a reset code.',
    },
    'forgot_send_code': {
      'uz': 'Kod yuborish', 'ru': 'Отправить код', 'en': 'Send code',
    },
    'reset_password_title': {
      'uz': 'Yangi parol', 'ru': 'Новый пароль', 'en': 'New password',
    },
    'reset_password_hint': {
      'uz': "Emailga yuborilgan kodni kiriting va yangi parolni tanlang.",
      'ru': 'Введите код из письма и новый пароль.',
      'en': 'Enter the code from your email and choose a new password.',
    },
    'reset_code_label': {
      'uz': 'Tasdiqlash kodi', 'ru': 'Код подтверждения', 'en': 'Verification code',
    },
    'reset_new_password': {
      'uz': 'Yangi parol', 'ru': 'Новый пароль', 'en': 'New password',
    },
    'reset_password_cta': {
      'uz': 'Parolni tiklash', 'ru': 'Восстановить пароль', 'en': 'Reset password',
    },
    'reset_password_success': {
      'uz': 'Parol yangilandi — endi kirishingiz mumkin.',
      'ru': 'Пароль обновлён — теперь можно войти.',
      'en': 'Password updated — you can sign in now.',
    },
    'logout_confirm_title': {
      'uz': 'Chiqishni tasdiqlaysizmi?', 'ru': 'Выйти?', 'en': 'Sign out?',
    },
    'logout_confirm_body': {
      'uz': "Keyingi safar qayta kirish uchun parol kerak.",
      'ru': 'В следующий раз потребуется пароль.',
      'en': "You'll need your password to sign in again.",
    },

    // ========================================================================
    // Onboarding
    // ========================================================================
    'onboarding_title_1': {
      'uz': "Har kuni nima pishirishni o'ylab qolmang",
      'ru': 'Не думайте каждый день, что готовить',
      'en': "Stop wondering what to cook every day",
    },
    'onboarding_title_2': {
      'uz': "Oila salomatligini hisobga olib menyu tuzamiz",
      'ru': 'Составляем меню с учётом здоровья семьи',
      'en': "We plan menus considering your family's health",
    },
    'onboarding_title_3': {
      'uz': "Xarid ro'yxati avtomatik tayyor bo'ladi",
      'ru': 'Список покупок готовится автоматически',
      'en': 'Shopping list is prepared automatically',
    },

    // ========================================================================
    // Dashboard
    // ========================================================================
    'dashboard_family_suffix': {'uz': 'oilasi', 'ru': 'семья', 'en': 'family'},
    'dashboard_greeting': {
      'uz': 'Assalomu alaykum,', 'ru': 'Здравствуйте,', 'en': 'Hello,',
    },
    'dashboard_today_menu': {'uz': 'Bugungi menyu', 'ru': 'Меню на сегодня', 'en': "Today's menu"},
    'dashboard_no_menu_title': {
      'uz': 'Bugungi menyu tayyor emas',
      'ru': 'Меню на сегодня не готово',
      'en': "Today's menu is not ready",
    },
    'dashboard_no_menu_subtitle': {
      'uz': 'Bir necha bosishda menyu tuzing',
      'ru': 'Составьте меню в пару кликов',
      'en': 'Create a menu in a few taps',
    },
    'dashboard_create_menu': {'uz': 'Menyu tuzish', 'ru': 'Составить меню', 'en': 'Create menu'},
    'dashboard_shopping_ready_title': {
      'uz': "Xarid ro'yxati tayyor", 'ru': 'Список покупок готов', 'en': 'Shopping list is ready',
    },
    'dashboard_shopping_count': {
      'uz': 'mahsulot · N kategoriya',
      'ru': 'товаров · N категорий',
      'en': 'products · N categories',
    },
    'dashboard_stat_members': {'uz': "a'zo", 'ru': 'членов', 'en': 'members'},
    'dashboard_stat_days': {'uz': 'kun', 'ru': 'дней', 'en': 'days'},
    'dashboard_stat_holiday': {'uz': 'Bayram', 'ru': 'Праздник', 'en': 'Holiday'},
    'meal_breakfast': {'uz': 'Nonushta', 'ru': 'Завтрак', 'en': 'Breakfast'},
    'meal_lunch': {'uz': 'Tushlik', 'ru': 'Обед', 'en': 'Lunch'},
    'meal_dinner': {'uz': 'Kechki', 'ru': 'Ужин', 'en': 'Dinner'},
    'meal_now_badge': {'uz': 'HOZIR', 'ru': 'СЕЙЧАС', 'en': 'NOW'},

    // ========================================================================
    // Menu list
    // ========================================================================
    'menu_your_title': {'uz': 'Sizning menyungiz', 'ru': 'Ваше меню', 'en': 'Your menu'},
    'menu_this_week': {'uz': 'Bu hafta', 'ru': 'Эта неделя', 'en': 'This week'},
    'menu_this_month': {'uz': 'Bu oy', 'ru': 'Этот месяц', 'en': 'This month'},
    'menu_days_7': {'uz': '7 kun', 'ru': '7 дней', 'en': '7 days'},
    'menu_days_30': {'uz': '30 kun', 'ru': '30 дней', 'en': '30 days'},
    'menu_stat_calories': {'uz': 'Kaloriya', 'ru': 'Калории', 'en': 'Calories'},
    'menu_stat_recipes': {'uz': 'Retsept', 'ru': 'Рецепты', 'en': 'Recipes'},
    'menu_stat_halal': {'uz': 'Halol', 'ru': 'Халяль', 'en': 'Halal'},
    'menu_status_today': {'uz': 'BUGUN', 'ru': 'СЕГОДНЯ', 'en': 'TODAY'},
    'menu_status_active': {'uz': 'FAOL', 'ru': 'АКТИВ', 'en': 'ACTIVE'},
    'menu_empty_title': {'uz': "Menyu hali yo'q", 'ru': 'Меню пока нет', 'en': 'No menu yet'},
    'menu_empty_subtitle': {
      'uz': 'Boshlash uchun yangi menyu yarating',
      'ru': 'Создайте новое меню, чтобы начать',
      'en': 'Create a new menu to get started',
    },
    'menu_switch_dialog_title_7': {
      'uz': '7 kunlik menyu tuzish?',
      'ru': 'Создать меню на 7 дней?',
      'en': 'Create 7-day menu?',
    },
    'menu_switch_dialog_title_30': {
      'uz': '30 kunlik menyu tuzish?',
      'ru': 'Создать меню на 30 дней?',
      'en': 'Create 30-day menu?',
    },
    'menu_switch_dialog_body': {
      'uz': "Hozirgi menyu saqlanadi, yangi bo'sh menyu yaratiladi.",
      'ru': 'Текущее меню сохранится, новое будет пустым.',
      'en': 'Current menu will be saved, a new empty one will be created.',
    },

    // ========================================================================
    // Day detail
    // ========================================================================
    'day_detail_title': {'uz': 'Kun menyusi', 'ru': 'Меню дня', 'en': 'Day menu'},
    'day_not_found': {'uz': 'Kun topilmadi', 'ru': 'День не найден', 'en': 'Day not found'},
    'meal_slot_main': {'uz': 'Asosiy', 'ru': 'Основное', 'en': 'Main'},
    'meal_slot_soup': {'uz': "Sho'rva", 'ru': 'Суп', 'en': 'Soup'},
    'meal_slot_salad': {'uz': 'Salat', 'ru': 'Салат', 'en': 'Salad'},
    'meal_slot_drink': {'uz': 'Ichimlik', 'ru': 'Напиток', 'en': 'Drink'},
    'meal_slot_bread': {'uz': 'Non', 'ru': 'Хлеб', 'en': 'Bread'},
    'meal_slot_dessert': {'uz': 'Shirinlik', 'ru': 'Десерт', 'en': 'Dessert'},
    'slot_add_pick': {'uz': '+ Tanlash', 'ru': '+ Выбрать', 'en': '+ Select'},
    'slot_remove_tooltip': {'uz': "Olib tashlash", 'ru': 'Удалить', 'en': 'Remove'},
    'picker_title_suffix': {'uz': 'tanlash', 'ru': 'выбрать', 'en': 'select'},
    'picker_recommended': {'uz': 'Sizga mos', 'ru': 'Подходит вам', 'en': 'For you'},
    'picker_empty': {
      'uz': "Mos retsept topilmadi.\nAllergiya yoki afzalliklarni yumshating.",
      'ru': 'Подходящий рецепт не найден.\nОслабьте аллергии или предпочтения.',
      'en': "No suitable recipe found.\nSoften allergies or preferences.",
    },
    'kcal': {'uz': 'kcal', 'ru': 'ккал', 'en': 'kcal'},
    'min_short': {'uz': 'daq', 'ru': 'мин', 'en': 'min'},
    'servings': {'uz': 'kishi', 'ru': 'порций', 'en': 'servings'},
    'hot': {'uz': 'Issiq', 'ru': 'Горячее', 'en': 'Hot'},
    'cold': {'uz': 'Salqin', 'ru': 'Холодное', 'en': 'Cold'},
    'meal': {'uz': 'ovqat', 'ru': 'блюдо', 'en': 'meal'},
    'recipe_button': {'uz': 'Retsept', 'ru': 'Рецепт', 'en': 'Recipe'},
    'swap_button': {'uz': 'Almashtirish', 'ru': 'Заменить', 'en': 'Swap'},

    // ========================================================================
    // Shopping
    // ========================================================================
    'shopping_title': {'uz': "Xarid ro'yxati", 'ru': 'Список покупок', 'en': 'Shopping list'},
    'shopping_menu_products_suffix': {
      'uz': 'kunlik menyu · N mahsulot',
      'ru': 'дневное меню · N товаров',
      'en': 'day menu · N products',
    },
    'shopping_no_menu_title': {
      'uz': "Xarid ro'yxati bo'sh",
      'ru': 'Список покупок пуст',
      'en': 'Shopping list is empty',
    },
    'shopping_no_menu_body': {
      'uz': "Avval menyu tuzing — xarid ro'yxati avtomatik yaraladi",
      'ru': 'Сначала составьте меню — список появится сам',
      'en': 'Create a menu first — the list is generated automatically',
    },
    'shopping_empty_body': {
      'uz': "Menyuga hali ovqat qo'shilmagan",
      'ru': 'В меню пока нет блюд',
      'en': 'No meals added to the menu yet',
    },
    'shopping_kgo_connected': {
      'uz': "Karzinka Go bilan bog'landi",
      'ru': 'Karzinka Go подключён',
      'en': 'Karzinka Go connected',
    },
    'shopping_kgo_selected': {'uz': 'Tanlangan:', 'ru': 'Выбрано:', 'en': 'Selected:'},
    'shopping_kgo_items_of': {'uz': 'ta', 'ru': 'шт', 'en': 'items'},
    'shopping_kgo_unavailable_badge': {
      'uz': "QIDIRISH KERAK",
      'ru': 'ПОИСК',
      'en': 'SEARCH',
    },
    'shopping_kgo_unavailable_title': {
      'uz': "K-Go da qo'lda qidirish kerak",
      'ru': 'Найти в K-Go вручную',
      'en': 'Search in K-Go manually',
    },
    'shopping_kgo_unavailable_sub': {
      'uz': "mahsulot · aksiyada emas, K-Go ilovasida qidirib toping",
      'ru': 'товар · не в акциях, найдите в K-Go',
      'en': 'item(s) · not on promo, search in K-Go app',
    },
    'shopping_transfer_cta': {
      'uz': "Karzinka Go ga o'tkazish",
      'ru': 'Отправить в Karzinka Go',
      'en': 'Send to Karzinka Go',
    },
    'shopping_no_selection': {
      'uz': 'Mahsulot tanlanmagan', 'ru': 'Товар не выбран', 'en': 'No items selected',
    },
    'shopping_category_purchased_suffix': {
      'uz': 'mahsulot · N sotib olindi',
      'ru': 'товар · куплено N',
      'en': 'items · N purchased',
    },
    'shopping_kgo_integration_future': {
      'uz': "Karzinka Go bilan integratsiya — kelajakda",
      'ru': 'Интеграция с Karzinka Go — в будущем',
      'en': 'Karzinka Go integration — coming soon',
    },
    'som': {'uz': "so'm", 'ru': 'сум', 'en': 'som'},
    'karzinka_open_app': {
      'uz': 'Karzinka Go ilovasini ochish',
      'ru': 'Открыть приложение Karzinka Go',
      'en': 'Open Karzinka Go app',
    },
    'karzinka_or_tap_each': {
      'uz': 'Yoki har mahsulotni alohida bosib Karzinka Go da oching:',
      'ru': 'Или откройте каждый товар в Karzinka Go отдельно:',
      'en': 'Or open each product in Karzinka Go individually:',
    },
    'karzinka_add': {
      'uz': "Ochish", 'ru': 'Открыть', 'en': 'Open',
    },
    'karzinka_open_failed': {
      'uz': "Karzinka ilovasini ochib bo'lmadi",
      'ru': 'Не удалось открыть Karzinka',
      'en': "Couldn't open Karzinka",
    },
    'karzinka_transfer_empty_body': {
      'uz': "Karzinka Go da mavjud mahsulotlarni belgilang",
      'ru': 'Отметьте товары, доступные в Karzinka Go',
      'en': 'Select items available in Karzinka Go',
    },

    // Ingredient kategoriyalari
    'cat_vegetable': {'uz': 'Sabzavotlar', 'ru': 'Овощи', 'en': 'Vegetables'},
    'cat_fruit': {'uz': 'Mevalar', 'ru': 'Фрукты', 'en': 'Fruits'},
    'cat_meat': {'uz': "Go'sht", 'ru': 'Мясо', 'en': 'Meat'},
    'cat_dairy': {'uz': 'Sut mahsulotlari', 'ru': 'Молочные', 'en': 'Dairy'},
    'cat_grain': {'uz': 'Don mahsulotlari', 'ru': 'Крупы', 'en': 'Grains'},
    'cat_spice': {'uz': 'Ziravorlar', 'ru': 'Специи', 'en': 'Spices'},
    'cat_oil': {'uz': 'Moylar', 'ru': 'Масла', 'en': 'Oils'},
    'cat_other': {'uz': 'Boshqa', 'ru': 'Прочее', 'en': 'Other'},

    // ========================================================================
    // Recipes
    // ========================================================================
    'recipes_title': {'uz': 'Retseptlar', 'ru': 'Рецепты', 'en': 'Recipes'},
    'recipes_total_suffix': {'uz': 'ta ovqat', 'ru': 'блюд', 'en': 'meals'},
    'recipes_search_hint': {
      'uz': 'Retsept qidirish...',
      'ru': 'Поиск рецепта...',
      'en': 'Search recipes...',
    },
    'recipes_all': {'uz': 'Barchasi', 'ru': 'Все', 'en': 'All'},
    'recipes_empty_title': {
      'uz': 'Retsept topilmadi', 'ru': 'Рецепт не найден', 'en': 'No recipes found',
    },
    'recipes_empty_body': {
      'uz': "Filter yoki qidiruv shartlarini o'zgartiring",
      'ru': 'Измените фильтры или запрос',
      'en': 'Try adjusting filters or search',
    },
    'recipe_cat_breakfast': {'uz': 'Nonushta', 'ru': 'Завтрак', 'en': 'Breakfast'},
    'recipe_cat_lunch': {'uz': 'Tushlik', 'ru': 'Обед', 'en': 'Lunch'},
    'recipe_cat_dinner': {'uz': 'Kechki', 'ru': 'Ужин', 'en': 'Dinner'},
    'recipe_cat_salad': {'uz': 'Salat', 'ru': 'Салат', 'en': 'Salad'},
    'recipe_cat_soup': {'uz': "Sho'rva", 'ru': 'Суп', 'en': 'Soup'},
    'recipe_cat_drink': {'uz': 'Ichimlik', 'ru': 'Напиток', 'en': 'Drink'},
    'recipe_cat_dessert': {'uz': 'Shirinlik', 'ru': 'Десерт', 'en': 'Dessert'},
    'recipe_cat_bread': {'uz': 'Non', 'ru': 'Хлеб', 'en': 'Bread'},
    'recipe_cat_snack': {'uz': 'Yengil', 'ru': 'Закуска', 'en': 'Snack'},

    // Recipe detail
    'recipe_ingredients': {'uz': 'Ingredientlar', 'ru': 'Ингредиенты', 'en': 'Ingredients'},
    'recipe_steps': {'uz': 'Tayyorlash', 'ru': 'Приготовление', 'en': 'Steps'},
    'recipe_allergen_warning': {
      'uz': 'Diqqat — bu ovqatda:',
      'ru': 'Внимание — блюдо содержит:',
      'en': 'Warning — this meal contains:',
    },

    // ========================================================================
    // Profile
    // ========================================================================
    'profile_title': {'uz': 'Profil', 'ru': 'Профиль', 'en': 'Profile'},
    'profile_section_family': {'uz': 'Oila', 'ru': 'Семья', 'en': 'Family'},
    'profile_section_app': {'uz': 'Ilova', 'ru': 'Приложение', 'en': 'App'},
    'profile_section_account': {'uz': 'Hisob', 'ru': 'Аккаунт', 'en': 'Account'},
    'profile_family_name': {'uz': 'Oila nomi', 'ru': 'Название семьи', 'en': 'Family name'},
    'profile_family_name_subtitle': {
      'uz': 'Yangi nomni kiriting',
      'ru': 'Введите новое название',
      'en': 'Enter new name',
    },
    'profile_city': {'uz': 'Shahar', 'ru': 'Город', 'en': 'City'},
    'profile_members': {'uz': "A'zolar", 'ru': 'Члены семьи', 'en': 'Members'},
    'profile_settings': {'uz': 'Sozlamalar', 'ru': 'Настройки', 'en': 'Settings'},
    'profile_notifications': {'uz': 'Bildiruvlar', 'ru': 'Уведомления', 'en': 'Notifications'},
    'profile_delete_account': {
      'uz': "Hisobni o'chirish", 'ru': 'Удалить аккаунт', 'en': 'Delete account',
    },
    'delete_account_title': {
      'uz': "Hisobni butunlay o'chirish?",
      'ru': 'Удалить аккаунт полностью?',
      'en': 'Delete account permanently?',
    },
    'delete_account_body': {
      'uz': "Hisobingiz, oilangiz va barcha menyular butunlay o'chiriladi. "
          "Bu amalni orqaga qaytarib bo'lmaydi. Tasdiqlash uchun parolingizni kiriting.",
      'ru': 'Аккаунт, семья и меню будут удалены навсегда. Это действие '
          'нельзя отменить. Введите пароль для подтверждения.',
      'en': "Your account, family, and all menus will be permanently deleted. "
          "This cannot be undone. Enter your password to confirm.",
    },
    'delete_account_cta': {
      'uz': "Hisobni o'chirish", 'ru': 'Удалить', 'en': 'Delete',
    },
    'delete_password_hint': {
      'uz': 'Joriy parol', 'ru': 'Текущий пароль', 'en': 'Current password',
    },
    'delete_password_required': {
      'uz': 'Parol kerak', 'ru': 'Введите пароль', 'en': 'Password required',
    },
    'profile_city_pick_title': {'uz': 'Shahar tanlash', 'ru': 'Выбор города', 'en': 'Pick a city'},
    'profile_city_pick_sub': {
      'uz': "Ob-havo shu shahar bo'yicha aniqlanadi",
      'ru': 'Погода определяется по этому городу',
      'en': 'Weather is based on this city',
    },
    'profile_members_count_suffix': {'uz': 'ta', 'ru': 'чел.', 'en': 'people'},

    // ========================================================================
    // Settings
    // ========================================================================
    'settings_title': {'uz': 'Sozlamalar', 'ru': 'Настройки', 'en': 'Settings'},
    'settings_section_language': {'uz': 'Til', 'ru': 'Язык', 'en': 'Language'},
    'settings_section_notifications': {
      'uz': 'Bildiruvlar', 'ru': 'Уведомления', 'en': 'Notifications',
    },
    'settings_section_about': {'uz': 'Ilova haqida', 'ru': 'О приложении', 'en': 'About'},
    'settings_push': {
      'uz': 'Push bildiruvlar', 'ru': 'Push уведомления', 'en': 'Push notifications',
    },
    'settings_meal_reminder': {
      'uz': 'Ovqat vaqti eslatmasi',
      'ru': 'Напоминание о еде',
      'en': 'Meal time reminder',
    },
    'settings_holiday_notif': {
      'uz': 'Bayram bildiruvlari', 'ru': 'Уведомления о праздниках', 'en': 'Holiday alerts',
    },
    'settings_version': {'uz': 'Versiya', 'ru': 'Версия', 'en': 'Version'},
    'settings_server': {'uz': 'Server', 'ru': 'Сервер', 'en': 'Server'},

    // ========================================================================
    // Notifications
    // ========================================================================
    'notifications_title': {'uz': 'Bildiruvlar', 'ru': 'Уведомления', 'en': 'Notifications'},
    'notifications_all_read': {
      'uz': 'Hammasi', 'ru': 'Все прочитано', 'en': 'Mark all',
    },
    'notifications_upcoming_holidays': {
      'uz': 'Yaqin bayramlar', 'ru': 'Ближайшие праздники', 'en': 'Upcoming holidays',
    },
    'notifications_section': {'uz': 'Bildiruvlar', 'ru': 'Уведомления', 'en': 'Notifications'},
    'notifications_new_count_suffix': {'uz': 'yangi', 'ru': 'новых', 'en': 'new'},
    'notifications_empty_title': {
      'uz': "Bildiruv yo'q", 'ru': 'Нет уведомлений', 'en': 'No notifications',
    },
    'notifications_empty_body': {
      'uz': "Yangiliklar bo'lganda shu yerda ko'rinadi",
      'ru': 'Новости появятся здесь',
      'en': 'News will appear here',
    },
    'notifications_no_holidays': {
      'uz': "Keyingi 30 kunda bayram yo'q",
      'ru': 'В ближайшие 30 дней праздников нет',
      'en': "No holidays in the next 30 days",
    },
    'notif_kind_menu': {'uz': 'Menyu', 'ru': 'Меню', 'en': 'Menu'},
    'notif_kind_holiday': {'uz': 'Bayram', 'ru': 'Праздник', 'en': 'Holiday'},
    'notif_kind_allergy': {
      'uz': 'Ogohlantirish', 'ru': 'Предупреждение', 'en': 'Warning',
    },
    'notif_kind_update': {'uz': 'Yangilanish', 'ru': 'Обновление', 'en': 'Update'},
    'notif_kind_general': {'uz': 'Umumiy', 'ru': 'Общее', 'en': 'General'},
    'notification_not_found': {
      'uz': 'Bildiruv topilmadi', 'ru': 'Уведомление не найдено', 'en': 'Notification not found',
    },
    'days_short': {'uz': 'kun', 'ru': 'дн', 'en': 'd'},

    // ========================================================================
    // Family
    // ========================================================================
    'family_create_title': {'uz': 'Oila yaratish', 'ru': 'Создать семью', 'en': 'Create family'},
    'family_name_label': {'uz': 'Oila nomi', 'ru': 'Название семьи', 'en': 'Family name'},
    'family_name_hint': {
      'uz': "Masalan: Sobirjanovlar", 'ru': 'Например: Собиржановы', 'en': 'e.g. Smiths',
    },
    'family_city_label': {'uz': 'Shahar', 'ru': 'Город', 'en': 'City'},
    'family_members_title': {"uz": "Oila a'zolari", 'ru': 'Члены семьи', 'en': 'Family members'},
    'family_members_subtitle': {
      'uz': "Har a'zo uchun sog'liq holatini kiriting",
      'ru': 'Укажите здоровье каждого члена',
      'en': 'Enter health info for each member',
    },
    'family_no_members_title': {
      'uz': "Hali a'zo yo'q", 'ru': 'Пока нет членов', 'en': 'No members yet',
    },
    'family_no_members_body': {
      'uz': "Menyu tuzish uchun avval oila a'zolarini qo'shing",
      'ru': 'Сначала добавьте членов семьи',
      'en': 'Add members to plan a menu',
    },
    'member_add_title': {"uz": "Yangi a'zo", "ru": 'Новый член', 'en': 'New member'},
    'member_edit_title': {
      "uz": "A'zoni tahrirlash", "ru": 'Изменить члена', 'en': 'Edit member',
    },
    'member_add_button': {"uz": "A'zo qo'shish", "ru": 'Добавить', 'en': 'Add member'},
    'member_delete_confirm_body': {
      'uz': "A'zo va uning ma'lumotlari butunlay o'chiriladi.",
      'ru': 'Член и его данные будут удалены.',
      'en': "Member and their data will be permanently deleted.",
    },
    'add_and_more': {
      "uz": "Qo'shib yana kiritish", "ru": 'Добавить и ещё', 'en': 'Add another',
    },
    'add_finish': {'uz': 'Tugatish', 'ru': 'Завершить', 'en': 'Finish'},
    'avatar_label': {'uz': 'Avatar', 'ru': 'Аватар', 'en': 'Avatar'},
    'name_label': {'uz': 'Ism', 'ru': 'Имя', 'en': 'Name'},
    'age_label': {'uz': 'Yosh', 'ru': 'Возраст', 'en': 'Age'},
    'gender_label': {'uz': 'Jinsi', 'ru': 'Пол', 'en': 'Gender'},
    'gender_male': {'uz': 'Erkak', 'ru': 'Мужской', 'en': 'Male'},
    'gender_female': {'uz': 'Ayol', 'ru': 'Женский', 'en': 'Female'},
    'years_old': {'uz': 'yosh', 'ru': 'лет', 'en': 'y.o.'},

    // Health conditions
    'health_optional_title': {
      "uz": "Sog'liq holati (ixtiyoriy)",
      'ru': 'Здоровье (по желанию)',
      'en': 'Health (optional)',
    },
    'health_optional_subtitle': {
      'uz': "Menyu shu asosda tuziladi",
      'ru': 'Меню составится с учётом этого',
      'en': 'The menu is planned accordingly',
    },
    'health_cat_allergy': {'uz': 'Allergiya', 'ru': 'Аллергия', 'en': 'Allergy'},
    'health_cat_diabetes': {'uz': 'Diabet', 'ru': 'Диабет', 'en': 'Diabetes'},
    'health_cat_heart': {'uz': 'Yurak', 'ru': 'Сердце', 'en': 'Heart'},
    'health_cat_obesity': {'uz': 'Vazn', 'ru': 'Вес', 'en': 'Weight'},
    'health_cat_other': {'uz': 'Boshqa', 'ru': 'Другое', 'en': 'Other'},
    'health_variants_selected': {
      "uz": 'variant · N tanlangan',
      'ru': 'вариантов · выбрано N',
      'en': 'options · N selected',
    },

    // Existing members
    'members_existing': {"uz": "Mavjud a'zolar", "ru": 'Существующие члены', 'en': 'Existing members'},
    'member_delete_confirm_suffix': {
      "uz": "ni o'chirish?", 'ru': ' удалить?', 'en': ' — delete?',
    },
  };

  /// Kalitni tilga qarab qaytaradi. Topilmasa kalitning o'zi.
  static String t(String key, String lang) {
    final entry = _strings[key];
    if (entry == null) return key;
    return entry[lang] ?? entry['uz'] ?? key;
  }
}
