"""Karzinka Lavka B2B API'ni tekshirish uchun.

Ishlatish:
    python manage.py probe_lavka                       # kategoriya daraxti
    python manage.py probe_lavka --category <CAT_ID>   # kategoriyadagi mahsulotlar
    python manage.py probe_lavka --all                 # butun katalog (uzoq)

.env'da KARZINKA_LAVKA_TOKEN, YAUID, GEOID o'rnatilgan bo'lishi kerak.
"""
import json

from django.core.management.base import BaseCommand

from apps.products.utils.karzinka_lavka import (
    fetch_all_products,
    fetch_category,
    fetch_category_group,
)


class Command(BaseCommand):
    help = "Yandex Lavka B2B API'ni tekshirish"

    def add_arguments(self, parser):
        parser.add_argument('--category', help="Bitta kategoriya ID'si")
        parser.add_argument('--group', default='', help="category_slug_path.group_id")
        parser.add_argument('--all', action='store_true', help='Butun katalog')
        parser.add_argument('--raw', action='store_true', help="Xom JSON javob")

    def handle(self, *args, **opts):
        if opts['all']:
            products = fetch_all_products()
            self.stdout.write(self.style.SUCCESS(f"JAMI: {len(products)} mahsulot"))
            for p in products[:20]:
                self.stdout.write(f"  {p.id}  {p.price:>8}  {p.title}")
            return

        if opts['category']:
            products = fetch_category(opts['category'], group_id=opts['group'])
            self.stdout.write(self.style.SUCCESS(f"Kategoriya: {len(products)} mahsulot"))
            for p in products:
                self.stdout.write(f"  {p.id}  {p.price:>8} so'm  {p.title}  ({p.amount})")
            return

        data = fetch_category_group()
        if data is None:
            self.stdout.write(self.style.ERROR("Javob yo'q. .env sozlamalarini tekshiring."))
            return

        if opts['raw']:
            self.stdout.write(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
        else:
            self.stdout.write(self.style.SUCCESS("Kategoriya daraxti keldi. Kalitlar:"))
            self.stdout.write(str(list(data.keys()) if isinstance(data, dict) else type(data)))
            self.stdout.write("\nBirinchi 2000 belgi:")
            self.stdout.write(json.dumps(data, ensure_ascii=False)[:2000])
