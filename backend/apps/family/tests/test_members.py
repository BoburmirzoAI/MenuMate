"""Family members: CRUD + valid/invalid inputs."""
from django.core.cache import cache

from apps.family.models.family import FamilyMember
from apps.shared.tests.utils import MenuMateAPITestCase


class FamilyMemberTests(MenuMateAPITestCase):
    LIST_URL = '/api/v1/family/members/'

    def setUp(self):
        cache.clear()
        self.user, _ = self.create_and_login(email='m@test.local')
        self.client.post('/api/v1/family/', data={
            'family_name': 'X', 'city': 'Y',
        }, format='json')

    def _detail(self, member_id: int) -> str:
        return f'{self.LIST_URL}{member_id}/'

    def test_list_empty(self):
        r = self.client.get(self.LIST_URL)
        body = self.assert_envelope_success(r, 200)
        self.assertEqual(body['data'], [])

    def test_create_valid(self):
        r = self.client.post(self.LIST_URL, data={
            'name': 'Ali', 'age': 30, 'gender': 'MALE',
        }, format='json')
        body = self.assert_envelope_success(r, 201)
        self.assertEqual(body['data']['name'], 'Ali')

    def test_create_invalid_age(self):
        r = self.client.post(self.LIST_URL, data={
            'name': 'X', 'age': 200, 'gender': 'MALE',
        }, format='json')
        self.assert_envelope_error(r, 400)

    def test_create_empty_name(self):
        r = self.client.post(self.LIST_URL, data={
            'name': '  ', 'age': 30, 'gender': 'MALE',
        }, format='json')
        self.assert_envelope_error(r, 400)

    def test_get_detail(self):
        r = self.client.post(self.LIST_URL, data={
            'name': 'Vali', 'age': 25, 'gender': 'MALE',
        }, format='json')
        mid = r.json()['data']['id']
        r = self.client.get(self._detail(mid))
        self.assert_envelope_success(r, 200)

    def test_detail_404(self):
        r = self.client.get(self._detail(999999))
        self.assert_envelope_error(r, 404, reason='member_not_found_or_wrong_family')

    def test_delete(self):
        r = self.client.post(self.LIST_URL, data={
            'name': 'X', 'age': 40, 'gender': 'FEMALE',
        }, format='json')
        mid = r.json()['data']['id']
        r = self.client.delete(self._detail(mid))
        self.assert_envelope_success(r, 200)
        self.assertFalse(FamilyMember.objects.filter(pk=mid).exists())

    def test_patch_invalid_recipe_id(self):
        r = self.client.post(self.LIST_URL, data={
            'name': 'X', 'age': 40, 'gender': 'FEMALE',
        }, format='json')
        mid = r.json()['data']['id']
        r = self.client.patch(self._detail(mid), data={
            'liked_recipe_ids': [999999],
        }, format='json')
        self.assert_envelope_error(r, 400, reason='unknown_recipe_ids')
