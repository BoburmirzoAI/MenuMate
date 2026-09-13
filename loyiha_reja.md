# 🍽️ Family Menu Planner — Loyiha Rejasi

---

## 📖 Loyiha Haqida To'liq Ma'lumot

### Loyiha Nomi
**Family Menu Planner** — Oilaviy ovqat menyu rejalashtiruvchi ilova

### Loyiha Maqsadi
Oila a'zolarining ovqat xohish-istaklari, allergiyalari va sog'liq holatlariga qarab avtomatik ravishda haftalik yoki oylik menyu tuzib beruvchi, kerakli mahsulotlarni hisoblab, xarid qilish imkoniyatini taqdim etuvchi mobil ilova yaratish.

---

## 🧩 Loyiha Funksiyalari (Feature List)

### 1. 👨‍👩‍👧‍👦 Oila va A'zolar Boshqaruvi
- Bitta foydalanuvchi (oila boshlig'i) ro'yxatdan o'tadi
- Oila a'zolarini qo'shadi (ism, yosh, jinsi)
- Har bir a'zo uchun quyidagilarni kiritadi:
  - Sevimli ovqatlar
  - Yoqtirmaydigan ovqatlar
  - Allergiyalar (dukkakli, sut, tuxum, yong'oq va h.k.)
  - Sog'liq holati (diabet, yurak kasalligi, semizlik va h.k.)
- Ilova allergiya va ovqat xohishi o'rtasida ziddiyat bo'lsa **ogohlantirish** beradi, lekin cheklov qo'ymaydi — foydalanuvchi o'zi qaror qiladi

### 2. 🍲 Retsept Bazasi
- Barcha ovqatlar, salatlar, ichimliklar ma'lumotlar bazasida saqlanadi
- Har bir retseptda quyidagilar bo'ladi:
  - Ovqat nomi (O'zbek, Rus, Ingliz tillarida)
  - Ingredientlar va miqdori (1 kishi uchun)
  - Tayyorlash bosqichlari
  - Tayyorlash vaqti
  - Kaloriya miqdori
  - Kategoriya (issiq ovqat, salat, ichimlik, non-mahsulot va h.k.)
  - Mavsum (yozgi, qishki, har doim)
  - Allergiya teglar (dukkakli, sut va h.k.)

### 3. 📅 Menyu Generatsiya Algoritmi
- Foydalanuvchi menyu davomiyligini tanlaydi:
  - **1 haftalik** menyu
  - **1 oylik** menyu
- Algoritm quyidagilarga asoslanib menyu tuzadi:
  - Oila a'zolarining xohishlari
  - Allergiya va sog'liq cheklovlari
  - Ob-havo ma'lumotlari (issiq kunda engil, sovuq kunda quvvatli ovqat)
  - Bayram kunlari (maxsus menyu tavsiyasi)
  - Ovqatlar takrorlanmasligi (bir haftada bir xil ovqat ko'p marta kelmasligi)
  - Balans (issiq ovqat, salat, ichimlik)
- Tuzilgan menyuni **customize qilish** imkoni:
  - Muayyan kunda ovqatni o'zgartirish
  - Ovqat o'rniga boshqasini tanlash
  - Kun menyusini qayta generatsiya qilish

### 4. 🛒 Mahsulot Hisoblash
- Tuzilgan menyuga asoslanib kerakli mahsulotlar ro'yxati chiqariladi
- Oila a'zolari soniga qarab miqdor hisoblanadi
- Masalan: 5 kishi, 7 kunlik menyu → **3 kg piyoz, 5 kg kartoshka, 2 litr sut** va h.k.
- Mahsulotlar kategoriyalar bo'yicha guruhlangan (sabzavotlar, go'sht, sut mahsulotlari va h.k.)

### 5. 🌤️ Ob-havo Integratsiyasi
- OpenWeatherMap API orqali foydalanuvchi shahridagi ob-havo olinadi
- **Issiq kunda** (25°C+): engil ovqatlar tavsiya qilinadi (salatlar, meva, qatiq)
- **Sovuq kunda** (10°C-): quvvatli va issiq ovqatlar tavsiya qilinadi (sho'rva, mastava)
- Ob-havo menyu algoritmiga ta'sir qiladi

### 6. 🎉 Bayram Bildiruvi
- O'zbekiston rasmiy bayramlari bazada saqlanadi:
  - Yangi yil, Navro'z, Mustaqillik kuni, Ramazon hayiti, Qurbon hayiti va h.k.
- Foydalanuvchi menyu tuzayotganda shu davr ichida bayram bo'lsa:
  - **Push notification** yuboriladi: "⚠️ 21-mart Navro'z bayrami — maxsus menyu tavsiya qilamiz"
  - Foydalanuvchi xohlasa bayram menyusiga o'tishi mumkin

### 7. 🛍️ Korzinka Go Integratsiyasi *(Keyinroq qo'shiladi)*
- Hisoblangan mahsulotlar ro'yxati Korzinka Go ilovasiga yuboriladi
- Qaysi mahsulotlar korzinkada bor, qaysilari yo'q ko'rsatiladi
- Umumiy summa hisoblanadi
- To'g'ridan-to'g'ri Korzinka Go orqali yetkazib berish buyurtma qilish mumkin
- To'lov Korzinka Go ichidan amalga oshiriladi

### 8. 🌍 Ko'p Til Qo'llab-quvvatlash
- **O'zbek tili** (asosiy)
- **Rus tili**
- **Ingliz tili**
- Foydalanuvchi tilni istalgan vaqt o'zgartira oladi

---

## 🏗️ Texnik Arxitektura

### Texnologiyalar

| Qism | Texnologiya |
|---|---|
| Mobile Frontend | Flutter (Dart) |
| Backend | Django REST Framework (Python) |
| Ma'lumotlar bazasi | PostgreSQL |
| Ob-havo API | OpenWeatherMap API |
| Push Notification | Firebase Cloud Messaging (FCM) |
| Autentifikatsiya | JWT (SimpleJWT) |
| Korzinka API | *(Keyinroq)* |

### Backend Tuzilmasi (Django Apps)

```
backend/
├── accounts/          # Foydalanuvchi, oila, a'zolar
├── recipes/           # Retseptlar bazasi
├── menu/              # Menyu generatsiya algoritmi
├── products/          # Mahsulot hisoblash
├── weather/           # Ob-havo integratsiya
├── notifications/     # Bayram va push bildiruv
└── korzinka/          # Korzinka Go integratsiya (keyinroq)
```

### Ma'lumotlar Bazasi Asosiy Modellari

```
User
├── id, email, password
└── oila → FamilyProfile

FamilyProfile
├── id, user, family_name, city
└── members → FamilyMember[]

FamilyMember
├── id, family, name, age, gender
├── liked_foods → Recipe[]
├── disliked_foods → Recipe[]
└── health_conditions → HealthCondition[]

HealthCondition
├── id, member
├── type (allergiya, diabet, yurak va h.k.)
└── ingredients → Ingredient[]  # allergiya bo'lsa

Recipe
├── id, name_uz, name_ru, name_en
├── category, season, calories
├── prep_time, servings
├── ingredients → RecipeIngredient[]
├── steps → RecipeStep[]
└── allergens → AllergenTag[]

Menu
├── id, family, start_date, end_date
├── duration_type (haftalik/oylik)
└── days → MenuDay[]

MenuDay
├── id, menu, date
└── meals → MenuMeal[]

MenuMeal
├── id, day, meal_type (nonushta/tushlik/kechki)
└── recipe → Recipe
```

### API Endpointlar

```
# Auth
POST   /api/auth/register/
POST   /api/auth/login/
POST   /api/auth/refresh/

# Oila
GET    /api/family/
POST   /api/family/
POST   /api/family/members/
PUT    /api/family/members/{id}/
DELETE /api/family/members/{id}/

# Retseptlar
GET    /api/recipes/
GET    /api/recipes/{id}/
POST   /api/recipes/            # Admin

# Menyu
POST   /api/menu/generate/      # Menyu generatsiya
GET    /api/menu/{id}/
PUT    /api/menu/{id}/meals/{meal_id}/  # Customize
POST   /api/menu/{id}/regenerate-day/  # Kun qayta generatsiya

# Mahsulotlar
GET    /api/menu/{id}/products/ # Mahsulot ro'yxati

# Ob-havo
GET    /api/weather/            # Joriy ob-havo

# Bayramlar
GET    /api/holidays/           # Yaqin bayramlar
```

---

## 📆 Bir Haftalik Reja (Kun Bo'yicha)

### 🗓️ 1-kun — Muhit va Backend Poydevor
**Maqsad:** Loyiha ishga tushsin, asosiy tuzilma tayyor bo'lsin

- [ ] Django loyihasi yaratish
- [ ] PostgreSQL ulash va sozlash
- [ ] Django apps yaratish (accounts, recipes, menu, products, weather, notifications)
- [ ] Asosiy modellarni yozish (User, FamilyProfile, FamilyMember, HealthCondition)
- [ ] JWT autentifikatsiya sozlash (SimpleJWT)
- [ ] Register va Login API yozish
- [ ] Migration va test

---

### 🗓️ 2-kun — Retsept Bazasi va Ma'lumot Kiritish
**Maqsad:** Retseptlar bazasi tayyor, kamida 50-100 ta ovqat kiritilgan bo'lsin

- [ ] Recipe, Ingredient, RecipeIngredient, AllergenTag modellarini yozish
- [ ] Retsept API (CRUD)
- [ ] Kamida 50 ta retsept ma'lumotlarini JSON da tayyorlash
- [ ] Fixture orqali bazaga yuklash
- [ ] Allergiya ogohlantirish logikasi

---

### 🗓️ 3-kun — Menyu Generatsiya Algoritmi
**Maqsad:** Asosiy algoritm ishlayotgan bo'lsin

- [ ] Menu, MenuDay, MenuMeal modellarini yozish
- [ ] Menyu generatsiya algoritmi:
  - Oila a'zolari xohishini hisobga olish
  - Allergiya tekshiruvi va ogohlantirish
  - Ovqat takrorlanmaslik logikasi
  - Nonushta / tushlik / kechki ovqat balansi
- [ ] Haftalik va oylik menyu generatsiya
- [ ] Menyu customize API (ovqat o'zgartirish)
- [ ] Test va debug

---

### 🗓️ 4-kun — Mahsulot Hisoblash va Tashqi API lar
**Maqsad:** Mahsulot hisobi va ob-havo ishlayotgan bo'lsin

- [ ] Mahsulot hisoblash algoritmi (oila soni × ingredientlar miqdori × kun soni)
- [ ] Mahsulotlar kategoriya bo'yicha guruhlash
- [ ] OpenWeatherMap API integratsiya
- [ ] Ob-havoga qarab menyu filtrlash logikasi
- [ ] Bayramlar bazasini yaratish (O'zbekiston bayramlari)
- [ ] Bayram ogohlantirish API

---

### 🗓️ 5-kun — Flutter Ilovasi (Asosiy Ekranlar)
**Maqsad:** Flutter ilovasi ishga tushsin, asosiy ekranlar tayyor bo'lsin

- [ ] Flutter loyihasi yaratish
- [ ] Ko'p til sozlash (flutter_localizations)
- [ ] HTTP client sozlash (dio yoki http package)
- [ ] JWT token saqlash (flutter_secure_storage)
- [ ] Ekranlar:
  - Kirish / Ro'yxatdan o'tish
  - Oila ma'lumotlari kiritish
  - Oila a'zolari boshqaruvi
  - A'zo xohish va allergiyalarini kiritish

---

### 🗓️ 6-kun — Flutter Ilovasi (Asosiy Funksiyalar)
**Maqsad:** Menyu va mahsulot ekranlar ishlayotgan bo'lsin

- [ ] Ekranlar:
  - Menyu generatsiya ekrani (davomiylik tanlash)
  - Menyu ko'rish ekrani (kunlar bo'yicha)
  - Menyu customize ekrani (ovqat o'zgartirish)
  - Mahsulotlar ro'yxati ekrani
  - Retsept detail ekrani
- [ ] Ob-havo ma'lumotini ko'rsatish
- [ ] Bayram ogohlantirish notification

---

### 🗓️ 7-kun — Polishing va Production Tayyorlash
**Maqsad:** Loyiha presentation ga tayyor bo'lsin

- [ ] UI/UX yaxshilash (ranglar, shriftlar, animatsiyalar)
- [ ] Xatolarni bartaraf etish (bug fixes)
- [ ] Loading state va error handling
- [ ] API dokumentatsiyasi (Swagger avtomatik)
- [ ] README.md yozish
- [ ] Backend server ga deploy qilish (Railway yoki Render — bepul)
- [ ] Oxirgi test

---

## 🗂️ Flutter Ekranlar Ro'yxati

```
1.  Splash Screen
2.  Onboarding (ilovani tanishtirish)
3.  Ro'yxatdan o'tish
4.  Kirish
5.  Bosh sahifa (Dashboard)
6.  Oila profili
7.  A'zo qo'shish / tahrirlash
8.  A'zo xohishlari
9.  Menyu generatsiya
10. Menyu ko'rish (haftalik/oylik)
11. Kun menyusi detail
12. Ovqat o'zgartirish
13. Retsept detail
14. Mahsulotlar ro'yxati
15. Sozlamalar (til, bildiruv)
```

---

## ⚠️ Muhim Eslatmalar

### Nima bilan boshlash kerak?
1. Avval **backend** ni yozasan — Flutter backend ga bog'liq
2. Har bir API ni yozib, **Postman** da test qilasan
3. Flutter ekranlarni yozishdan oldin **mock data** bilan test qilasan

### Production Level uchun:
- Har doim `try/except` bilan xatolarni ushla
- API response da `status`, `message`, `data` bo'lsin
- Parolni hech qachon ochiq saqla — bcrypt/hashing
- `.env` fayl ishlatasan (SECRET_KEY, DB, API keys)
- `requirements.txt` yozib qo'yasan

### Vaqt yetmasa prioritet:
1. ✅ Autentifikatsiya (Login/Register)
2. ✅ Oila a'zolari boshqaruvi
3. ✅ Retsept bazasi
4. ✅ Menyu generatsiya
5. ✅ Mahsulot hisoblash
6. 🔶 Ob-havo integratsiya
7. 🔶 Bayram bildiruvi
8. 🔷 Korzinka Go (keyinroq)

---

## 🚀 Texnologiyalar O'rnatish

```bash
# Backend
pip install django djangorestframework
pip install djangorestframework-simplejwt
pip install psycopg2-binary python-decouple
pip install requests  # Ob-havo API uchun
pip install django-cors-headers

# Flutter
flutter create family_menu_planner
cd family_menu_planner
# pubspec.yaml ga qo'shiladi:
# dio, flutter_secure_storage, flutter_localizations
# provider yoki riverpod (state management)
```

---

*Loyiha muallifi: Backend Intern*  
*Texnologiyalar: Django REST Framework + Flutter + PostgreSQL*  
*Versiya: 1.0 | Sana: 2026*
