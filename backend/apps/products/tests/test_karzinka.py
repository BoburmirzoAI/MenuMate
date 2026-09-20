"""Karzinka: in_stock parsing + aksiya sanasi filtri."""
from datetime import date
from django.test import TestCase

from apps.products.utils.karzinka import (
    _derive_in_stock,
    _parse_promotion_end,
)


class ParsePromotionEndTests(TestCase):
    def test_valid_range(self):
        tags = [{'id': 2, 'value': '17.09.2026-23.09.2026'}]
        self.assertEqual(_parse_promotion_end(tags), date(2026, 9, 23))

    def test_multiple_tags_picks_range(self):
        tags = [{'id': 3, 'value': '17'}, {'id': 2, 'value': '01.01.2027-15.01.2027'}]
        self.assertEqual(_parse_promotion_end(tags), date(2027, 1, 15))

    def test_none_or_empty(self):
        self.assertIsNone(_parse_promotion_end(None))
        self.assertIsNone(_parse_promotion_end([]))

    def test_invalid_format_returns_none(self):
        self.assertIsNone(_parse_promotion_end([{'value': 'bad-format'}]))

    def test_malformed_tag_object_ignored(self):
        self.assertIsNone(_parse_promotion_end([None, 'string', {'no_value': 'x'}]))


class DeriveInStockTests(TestCase):
    def test_promotion_active_today_returns_true(self):
        today = date(2026, 9, 20)
        self.assertTrue(_derive_in_stock({}, date(2026, 9, 23), today))

    def test_promotion_ended_yesterday_returns_false(self):
        today = date(2026, 9, 20)
        self.assertFalse(_derive_in_stock({}, date(2026, 9, 19), today))

    def test_no_promotion_defaults_to_true(self):
        self.assertTrue(_derive_in_stock({}, None, date(2026, 9, 20)))

    def test_explicit_in_stock_field_overrides_promo(self):
        p = {'in_stock': False}
        self.assertFalse(_derive_in_stock(p, date(2027, 1, 1), date(2026, 9, 20)))

    def test_sold_out_field(self):
        self.assertFalse(_derive_in_stock({'sold_out': True}, None, date(2026, 9, 20)))
        self.assertTrue(_derive_in_stock({'sold_out': False}, None, date(2026, 9, 20)))

    def test_numeric_stock(self):
        self.assertTrue(_derive_in_stock({'stock': 5}, None, date(2026, 9, 20)))
        self.assertFalse(_derive_in_stock({'stock': 0}, None, date(2026, 9, 20)))

    def test_stock_status_string(self):
        p1 = {'stock_status': 'in_stock'}
        p2 = {'stock_status': 'out_of_stock'}
        self.assertTrue(_derive_in_stock(p1, None, date(2026, 9, 20)))
        self.assertFalse(_derive_in_stock(p2, None, date(2026, 9, 20)))
