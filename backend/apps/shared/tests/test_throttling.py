"""Rate limiting — login throttle default 5/min."""
from django.core.cache import cache

from apps.shared.tests.utils import MenuMateAPITestCase


class LoginThrottleTests(MenuMateAPITestCase):
    URL = '/api/v1/users/login/'

    def setUp(self):
        cache.clear()

    def test_login_throttle_blocks_after_default_limit(self):
        codes = []
        for _ in range(10):
            r = self.client.post(self.URL, data={
                'email': 'nobody@test.local', 'password': 'x',
            }, format='json')
            codes.append(r.status_code)
        self.assertIn(429, codes, f'Kutilgan 429 topilmadi: {codes}')
        first_429 = codes.index(429)
        self.assertLessEqual(first_429, 5, f'429 juda kech: index {first_429}')

    def test_throttled_response_envelope(self):
        for _ in range(6):
            self.client.post(self.URL, data={
                'email': 'x@x.com', 'password': 'x',
            }, format='json')
        r = self.client.post(self.URL, data={
            'email': 'x@x.com', 'password': 'x',
        }, format='json')
        self.assertEqual(r.status_code, 429)
        body = r.json()
        self.assertFalse(body['success'])
        self.assertEqual(body['id'], 'THROTTLED')
