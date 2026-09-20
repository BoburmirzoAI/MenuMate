"""Auth flow: register, login, refresh, me, logout — envelope + xatolar."""
from django.core.cache import cache

from apps.shared.tests.utils import MenuMateAPITestCase
from apps.users.models.users import User


class RegisterTests(MenuMateAPITestCase):
    URL = '/api/v1/users/register/'

    def setUp(self):
        cache.clear()

    def test_register_valid(self):
        r = self.client.post(self.URL, data={
            'email': 'new@test.local',
            'password': 'StrongPass123!!',
            'password_confirm': 'StrongPass123!!',
            'first_name': 'New',
        }, format='json')
        body = self.assert_envelope_success(r, 201)
        self.assertIn('tokens', body['data'])
        self.assertIn('access', body['data']['tokens'])
        self.assertTrue(User.objects.filter(email='new@test.local').exists())

    def test_register_short_password(self):
        r = self.client.post(self.URL, data={
            'email': 'x@test.local', 'password': 'abc', 'password_confirm': 'abc',
        }, format='json')
        self.assert_envelope_error(r, 400)

    def test_register_password_mismatch(self):
        r = self.client.post(self.URL, data={
            'email': 'x@test.local',
            'password': 'StrongPass123!!',
            'password_confirm': 'OtherPass456!!',
        }, format='json')
        body = self.assert_envelope_error(r, 400)
        self.assertEqual(body['id'], 'PASSWORDS_DO_NOT_MATCH')
        self.assertEqual(body['errors']['reason'], 'password_confirm_mismatch')

    def test_register_duplicate_email(self):
        self.create_user(email='taken@test.local')
        r = self.client.post(self.URL, data={
            'email': 'taken@test.local',
            'password': 'StrongPass123!!',
            'password_confirm': 'StrongPass123!!',
        }, format='json')
        body = self.assert_envelope_error(r, 400, reason='email_already_registered')
        self.assertEqual(body['errors']['field'], 'email')

    def test_register_invalid_email(self):
        r = self.client.post(self.URL, data={
            'email': 'not-an-email',
            'password': 'StrongPass123!!',
            'password_confirm': 'StrongPass123!!',
        }, format='json')
        self.assert_envelope_error(r, 400)


class LoginTests(MenuMateAPITestCase):
    URL = '/api/v1/users/login/'

    def setUp(self):
        cache.clear()
        self.user = self.create_user(email='user@test.local', password='TestPass123!!')

    def test_login_valid(self):
        r = self.client.post(self.URL, data={
            'email': 'user@test.local', 'password': 'TestPass123!!',
        }, format='json')
        body = self.assert_envelope_success(r, 200)
        self.assertEqual(body['data']['user']['email'], 'user@test.local')
        self.assertIn('access', body['data']['tokens'])

    def test_login_wrong_password(self):
        r = self.client.post(self.URL, data={
            'email': 'user@test.local', 'password': 'WRONG!',
        }, format='json')
        body = self.assert_envelope_error(r, 400, reason='wrong_password')
        self.assertEqual(body['errors']['field'], 'password')

    def test_login_unknown_email(self):
        r = self.client.post(self.URL, data={
            'email': 'nobody@test.local', 'password': 'x',
        }, format='json')
        self.assert_envelope_error(r, 400, reason='user_not_found_or_deleted')

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        r = self.client.post(self.URL, data={
            'email': 'user@test.local', 'password': 'TestPass123!!',
        }, format='json')
        self.assert_envelope_error(r, 403, reason='user_deactivated')


class MeTests(MenuMateAPITestCase):
    URL = '/api/v1/users/me/'

    def test_me_no_token(self):
        r = self.client.get(self.URL)
        self.assertIn(r.status_code, (401, 403))

    def test_me_with_token(self):
        _, _ = self.create_and_login(email='u1@test.local')
        r = self.client.get(self.URL)
        body = self.assert_envelope_success(r, 200)
        self.assertEqual(body['data']['email'], 'u1@test.local')

    def test_me_patch_updates_profile(self):
        self.create_and_login(email='u2@test.local')
        r = self.client.patch(self.URL, data={'first_name': 'Renamed'}, format='json')
        body = self.assert_envelope_success(r, 200)
        self.assertEqual(body['data']['first_name'], 'Renamed')


class RefreshTests(MenuMateAPITestCase):
    def setUp(self):
        cache.clear()
        self.create_user(email='r@test.local')
        r = self.client.post('/api/v1/users/login/', data={
            'email': 'r@test.local', 'password': 'TestPass123!!',
        }, format='json')
        self.refresh_token = r.json()['data']['tokens']['refresh']

    def test_refresh_valid(self):
        r = self.client.post('/api/v1/users/refresh/', data={
            'refresh': self.refresh_token,
        }, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertIn('access', r.json())

    def test_refresh_invalid_token(self):
        r = self.client.post('/api/v1/users/refresh/', data={
            'refresh': 'not-a-token',
        }, format='json')
        self.assertEqual(r.status_code, 401)
