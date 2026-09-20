"""Admin: users CRUD."""
from django.core.cache import cache

from apps.shared.tests.utils import MenuMateAPITestCase
from apps.users.models.users import User


class AdminUsersTests(MenuMateAPITestCase):
    LIST_URL = '/api/v1/admin/users/'

    def setUp(self):
        cache.clear()
        self.admin, _ = self.create_and_login(
            email='admin@test.local', is_staff=True, is_superuser=True,
        )

    def _detail(self, uid: int) -> str:
        return f'{self.LIST_URL}{uid}/'

    def test_list_requires_admin(self):
        self.client.credentials()
        _, _ = self.create_and_login(email='plain@test.local')
        r = self.client.get(self.LIST_URL)
        self.assertIn(r.status_code, (401, 403))

    def test_list_returns_users(self):
        r = self.client.get(self.LIST_URL)
        body = self.assert_envelope_success(r, 200)
        self.assertIsInstance(body['data'], list)
        emails = [u['email'] for u in body['data']]
        self.assertIn('admin@test.local', emails)

    def test_create_valid(self):
        r = self.client.post(self.LIST_URL, data={
            'email': 'created@test.local', 'password': 'StrongPass123!!',
        }, format='json')
        body = self.assert_envelope_success(r, 201)
        self.assertEqual(body['data']['email'], 'created@test.local')

    def test_create_short_password(self):
        r = self.client.post(self.LIST_URL, data={
            'email': 'x@test.local', 'password': 'abc',
        }, format='json')
        self.assert_envelope_error(r, 400)

    def test_get_detail_404(self):
        r = self.client.get(self._detail(999999))
        self.assert_envelope_error(r, 404, reason='user_not_found_or_deleted')

    def test_patch_updates_profile(self):
        u = self.create_user(email='patch@test.local')
        r = self.client.patch(self._detail(u.pk), data={
            'first_name': 'Renamed',
        }, format='json')
        self.assert_envelope_success(r, 200)

    def test_delete_regular_user(self):
        u = self.create_user(email='delete@test.local')
        r = self.client.delete(self._detail(u.pk))
        self.assert_envelope_success(r, 200)

    def test_delete_superuser_refused(self):
        r = self.client.delete(self._detail(self.admin.pk))
        self.assert_envelope_error(r, 400, reason='cannot_delete_superuser')

    def test_set_password_valid(self):
        u = self.create_user(email='pwd@test.local')
        r = self.client.post(f'{self._detail(u.pk)}set-password/', data={
            'password': 'NewSecure123!!',
        }, format='json')
        self.assert_envelope_success(r, 200)
        u.refresh_from_db()
        self.assertTrue(u.check_password('NewSecure123!!'))
