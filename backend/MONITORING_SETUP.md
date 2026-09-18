# Sentry & Rate limiting sozlash

## 1. Sentry (xato monitoringi)

### Nima uchun kerak?
Production'da yuzaga kelgan xatolarni (500 errorlar, exception'lar, crash'lar) real vaqtda kuzatib borish. Foydalanuvchidan shikoyat kutmasdan darhol bilib olish.

### Sozlash

1. https://sentry.io da bepul akkaunt oching → yangi Django loyihasi yarating
2. DSN URL'ni oling (masalan: `https://abc123@o12345.ingest.sentry.io/67890`)
3. `.env` fayl'iga qo'shing:

```env
SENTRY_DSN=https://abc123@o12345.ingest.sentry.io/67890
SENTRY_ENVIRONMENT=production
SENTRY_RELEASE=1.0.0
```

4. `poetry install` ishga tushiring — `sentry-sdk` avtomatik o'rnatiladi

**Muhim:** `SENTRY_DSN` bo'sh bo'lsa Sentry umuman ishga tushmaydi (dev muhitida
xato dashboard'ni to'ldirmaslik uchun).

### Nimalar yuboriladi?
- Django view'lardagi exception'lar
- Celery task'larida yuzaga kelgan xatolar
- Redis xatolari
- `logger.error()` yordamida yozilgan xatolar (breadcrumb sifatida INFO+ ham)
- 10% so'rovlar uchun performance metrikalari (traces_sample_rate=0.1)

### Nimalar YUBORILMAYDI (xavfsizlik uchun)?
- Foydalanuvchi email/paroli (`send_default_pii=False`)
- Katta hajmli request body'lar (`request_bodies='small'`)

---

## 2. Rate limiting (DRF throttling)

### Cheklovlar ro'yxati

| Endpoint | Chastota | Asos |
|---------|---------|------|
| `POST /users/login/` | **5/daq** | Brute-force parol urish |
| `POST /users/register/` | **5/soat** | Fake akkaunt spam'i |
| `POST /users/forgot-password/` | **5/soat** | Email spam / bomb |
| `POST /users/reset-password/` | **5/soat** | Email spam / bomb |
| `POST /menu/menus/` | **5/daq** | Og'ir hisoblash (recipe filter + shuffle) |
| `POST /admin/notifications/broadcast/` | **10/soat** | Admin xato push spam |
| Boshqa API (anon) | **60/daq** | DDoS ehtiyot |
| Boshqa API (auth) | **300/daq** | Foydalanuvchi qulayligi |

### Sozlash
Chastotalarni `core/settings/base.py` → `REST_FRAMEWORK.DEFAULT_THROTTLE_RATES` da o'zgartirasiz. Format: `<son>/<vaqt>` — `sec`, `min`, `hour`, `day`.

### Kimga qarshi hisoblanadi?
- **Anonim so'rov** → IP manzil bo'yicha (reverse-proxy orqasidan xafflamaydi — DRF `X-Forwarded-For`'ni to'g'ri o'qiydi)
- **Autentifikatsiya qilingan foydalanuvchi** → `user.pk` bo'yicha (IP muhim emas)

### 429 javob namunasi
```json
{
    "success": false,
    "id": "THROTTLED",
    "message": "So'rov cheklandi. Keyinroq qayta urinib ko'ring"
}
```

Frontend/mobile bu 429 kelganda foydalanuvchiga "Ko'p urinish, biroz kuting" degan xabar ko'rsatish kerak.

### Redis cache majburiy
Throttling counter'lari Django cache orqali yuritiladi. Multi-worker gunicorn'da har worker'da alohida counter bo'lmasligi uchun `prod.py` da Redis backend belgilangan (`REDIS_CACHE_URL` env orqali).

---

## Testlash

### Sentry test
```python
# Django shell yoki view'da
from sentry_sdk import capture_message
capture_message("Test message from Menu Mate")
```

Yoki qasddan xato yarating — view'da `raise Exception("test")`.

### Rate limit test
```bash
# Login endpoint'ni 6 marta ketma-ket urinib ko'ring:
for i in {1..6}; do
  curl -X POST https://api.menumate.uz/api/v1/users/login/ \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"wrong"}'
  echo
done
# 6-so'rovda 429 keladi
```
