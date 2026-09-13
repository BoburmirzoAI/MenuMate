# Menu Mate — Admin Panel

Django REST backend uchun **web admin panel**. Vite + React 19 + TypeScript
zamiga qurilgan. Dark theme + terracotta accent (Menu Mate brand'iga mos).

Bu panel Django o'zining `/admin/` panelini almashtirmaydi — u tez debug uchun
qoladi. React admin esa **biznes ish uchun** (retseptlarni ko'zdan kechirish,
foydalanuvchi ma'lumotlari, bildirishnomalar, statistika) yozilgan.

---

## Texnologiyalar

| Qatlam | Kutubxona | Nima uchun |
|---|---|---|
| Base | React 19 + TypeScript 5.7 + Vite 6 | Fast dev, strict types |
| Routing | react-router-dom v7 | Data router API |
| Server state | @tanstack/react-query | Cache + invalidation |
| Client state | zustand | Auth store (2KB) |
| HTTP | axios | Interceptor + refresh flow |
| Forms | react-hook-form + zod | Type-safe validatsiya |
| Icons | lucide-react | Zamonaviy, tree-shakable |
| Charts | recharts | Responsive area/bar |
| Styling | Vanilla CSS + CSS Modules | Framework'siz, aniq scoped |

Tailwind, UI kit yoki boshqa keng framework **ishlatilmagan** —
loyihaning brand hissini custom tokenlar bilan boshqarish qulayroq.

---

## Papka strukturasi

```
admin/
├── index.html
├── package.json
├── vite.config.ts               # /api → localhost:8000 proksi
├── tsconfig.*.json              # strict TS + path alias
├── eslint.config.js
├── public/
│   └── favicon.svg
└── src/
    ├── main.tsx                 # React entry
    ├── App.tsx                  # Provider'lar (Query + Router)
    │
    ├── styles/
    │   ├── tokens.css           # Rang/spacing/radius o'zgaruvchilari
    │   └── globals.css          # Reset + Inter/Fraunces
    │
    ├── shared/                  # Barcha feature'lar foydalanadigan qatlam
    │   ├── api/
    │   │   ├── client.ts        # Axios + JWT interceptor + refresh
    │   │   ├── endpoints.ts     # URL literal'lari
    │   │   └── types.ts         # ApiSuccess/Failure/Paginated + ApiError
    │   ├── auth/
    │   │   ├── store.ts         # Zustand (user, tokens, login/logout)
    │   │   ├── ProtectedRoute.tsx
    │   │   └── PublicRoute.tsx
    │   ├── ui/                  # Umumiy komponentlar
    │   │   ├── Button/
    │   │   ├── Card/
    │   │   ├── Input/
    │   │   ├── Badge/
    │   │   ├── Spinner/
    │   │   ├── Skeleton/
    │   │   ├── EmptyState/
    │   │   ├── PageHeader/
    │   │   └── index.ts         # Barrel — `@shared/ui` orqali import
    │   └── layout/
    │       ├── AppShell.tsx     # Sidebar + Topbar + <Outlet />
    │       ├── Sidebar.tsx
    │       ├── Topbar.tsx
    │       └── navItems.ts      # Menyu ro'yxati
    │
    ├── features/                # Feature-first — har biri mustaqil
    │   ├── auth/
    │   │   └── LoginPage.tsx
    │   └── dashboard/
    │       ├── DashboardPage.tsx
    │       └── StatCard.tsx
    │
    ├── router/
    │   ├── routes.tsx           # createBrowserRouter
    │   ├── paths.ts             # URL literal'lari
    │   └── NotFoundPage.tsx
    │
    └── types/
        └── domain.ts            # Backend model'lari (User, Recipe, Menu, …)
```

### Konvensiyalar

- **Feature-first** — bir vazifaga tegishli hamma narsa (`XPage`, `XForm`,
  `useXQuery`, `X.module.css`) o'sha `features/x/` ostida turadi. Boshqa
  feature'lar unga kirmaydi; umumiylik kerak bo'lsa `shared/` ga chiqadi.
- **Har komponent — o'z papka** — `Button/Button.tsx` + `Button/Button.module.css`.
  Barcha stillar CSS Modules, aniq scoped. Global stil faqat `styles/globals.css`.
- **CSS o'zgaruvchilari** — hech qanday hex kod komponent CSS'ida yozilmaydi.
  Faqat `var(--color-accent)`, `var(--space-4)`.
- **TypeScript** — `strict: true`, `noUnusedLocals`, `noUnusedParameters`,
  `exactOptionalPropertyTypes`. `any` — taqiqlangan.
- **Path alias** — `@shared/*`, `@features/*`, `@styles/*`, `@router/*`,
  `@types/*`. Nisbiy `../../` yo'llar keraksiz.
- **Har public funksiya/komponent** — JSDoc bilan qisqa izoh. Nima uchun ishlashi
  kod'dan aniq bo'lmaydigan qismlarga sabab yoziladi.

---

## Ishga tushirish

### Talab

- Node.js **>=20**
- Menu Mate backend `docker compose up -d` bilan ishlab turgan (localhost:8000).

### Qadamlar

```bash
cd admin
cp .env.example .env         # Standart qiymatlar yetarli
npm install
npm run dev                  # http://localhost:5173
```

Dev-server `/api/*` so'rovlarni backend'ga proksi qiladi — CORS tashvishi yo'q.

### Buyruqlar

```bash
npm run dev         # Vite dev-server (HMR)
npm run build       # Prod build: tsc -b && vite build → dist/
npm run preview     # Prod build'ni lokalda tekshirish
npm run lint        # ESLint
npm run typecheck   # tsc --noEmit
```

---

## Login

Backend ishlab turgani sharti bilan superuser akkaunt yarating:

```bash
cd /Users/Developer/DRF/Menu\ Mate
docker compose exec backend python manage.py createsuperuser
```

Keyin http://localhost:5173/login sahifasidan kiring.

---

## Yangi sahifa qo'shish (namuna)

1. `src/features/<name>/<Name>Page.tsx` va `<Name>Page.module.css` yozing.
2. Kerak bo'lsa `src/features/<name>/api.ts` — TanStack Query hooks.
3. `src/router/paths.ts` va `src/router/routes.tsx` ga route qo'shing.
4. `src/shared/layout/navItems.ts` da menyu bandini `disabled` dan olib tashlang.

Har sahifa `<PageHeader>` bilan boshlanadi, `<Card>` bilan struktura oladi va
yuklanish holatini `<Skeleton>` yoki `<Spinner>` bilan ko'rsatadi. Bo'sh holat —
`<EmptyState>`. Bu — bir xil his beruvchi UX.

---

## Hozirgi progress

- ✅ Infrastruktura: Vite, TS, alias'lar, ESLint
- ✅ Dizayn tokenlari (dark + terracotta)
- ✅ API client + JWT auto refresh
- ✅ Auth store + ProtectedRoute/PublicRoute
- ✅ Umumiy UI komponentlari (8 ta)
- ✅ AppShell + Sidebar + Topbar
- ✅ Login page
- ✅ Dashboard skeleton (demo data)
- ⬜ Foydalanuvchilar, Retseptlar, Ingredientlar, Menyular sahifalari
- ⬜ Rollar va ruxsatlar sahifasi
- ⬜ Bildirishnomalar / bayramlar boshqaruvi
- ⬜ Toast tizimi (Sonner yoki custom)
