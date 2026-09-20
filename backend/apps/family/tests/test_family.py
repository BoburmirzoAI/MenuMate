"""Family profile: get / create / patch / delete + xatolar."""
from django.core.cache import cache

from apps.family.models.family import FamilyProfile
from apps.shared.tests.utils import MenuMateAPITestCase


class FamilyProfileTests(MenuMateAPITestCase):
    URL = '/api/v1/family/'

    def setUp(self):
        cache.clear()
        self.user, _ = self.create_and_login(email='f@test.local')

    def test_get_before_create_returns_404(self):
        r = self.client.get(self.URL)
        self.assert_envelope_error(r, 404, reason='user_has_no_family')

    def test_create_valid(self):
        r = self.client.post(self.URL, data={
            'family_name': 'Test oila', 'city': 'Tashkent',
        }, format='json')
        body = self.assert_envelope_success(r, 201)
        self.assertEqual(body['data']['family_name'], 'Test oila')
        self.assertTrue(FamilyProfile.objects.filter(user=self.user).exists())

    def test_create_twice_returns_400(self):
        self.client.post(self.URL, data={'family_name': 'A', 'city': 'X'}, format='json')
        r = self.client.post(self.URL, data={'family_name': 'B', 'city': 'X'}, format='json')
        self.assert_envelope_error(r, 400, reason='user_already_has_family')

    def test_create_empty_name(self):
        r = self.client.post(self.URL, data={
            'family_name': '   ', 'city': 'Tashkent',
        }, format='json')
        self.assert_envelope_error(r, 400)

    def test_get_after_create(self):
        self.client.post(self.URL, data={'family_name': 'X', 'city': 'Y'}, format='json')
        r = self.client.get(self.URL)
        body = self.assert_envelope_success(r, 200)
        self.assertEqual(body['data']['family_name'], 'X')

    def test_patch(self):
        self.client.post(self.URL, data={'family_name': 'X', 'city': 'Y'}, format='json')
        r = self.client.patch(self.URL, data={'family_name': 'New Name'}, format='json')
        body = self.assert_envelope_success(r, 200)
        self.assertEqual(body['data']['family_name'], 'New Name')

    def test_delete(self):
        self.client.post(self.URL, data={'family_name': 'X', 'city': 'Y'}, format='json')
        r = self.client.delete(self.URL)
        self.assert_envelope_success(r, 200)
        self.assertFalse(FamilyProfile.objects.filter(user=self.user).exists())

    def test_no_auth(self):
        self.client.credentials()
        r = self.client.get(self.URL)
        self.assertIn(r.status_code, (401, 403))
