"""Change / forgot / reset password."""
from django.core.cache import cache

from apps.shared.tests.utils import MenuMateAPITestCase


class ChangePasswordTests(MenuMateAPITestCase):
    URL = '/api/v1/users/me/change-password/'
    OLD = 'OldPass123!!'
    NEW = 'NewPass456!!'

    def setUp(self):
        cache.clear()
        self.user, _ = self.create_and_login(email='cp@test.local', password=self.OLD)

    def test_change_valid(self):
        r = self.client.post(self.URL, data={
            'old_password': self.OLD,
            'new_password': self.NEW,
            'new_password_confirm': self.NEW,
        }, format='json')
        self.assert_envelope_success(r, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.NEW))

    def test_change_wrong_old(self):
        r = self.client.post(self.URL, data={
            'old_password': 'WRONG!',
            'new_password': self.NEW,
            'new_password_confirm': self.NEW,
        }, format='json')
        self.assert_envelope_error(r, 400, reason='wrong_old_password')

    def test_change_mismatch(self):
        r = self.client.post(self.URL, data={
            'old_password': self.OLD,
            'new_password': self.NEW,
            'new_password_confirm': 'Different123!!',
        }, format='json')
        self.assert_envelope_error(r, 400, reason='password_confirm_mismatch')

    def test_change_same_as_old(self):
        r = self.client.post(self.URL, data={
            'old_password': self.OLD,
            'new_password': self.OLD,
            'new_password_confirm': self.OLD,
        }, format='json')
        self.assert_envelope_error(r, 400, reason='new_password_same_as_old')


class ForgotPasswordTests(MenuMateAPITestCase):
    URL = '/api/v1/users/forgot-password/'

    def setUp(self):
        cache.clear()
        self.create_user(email='fp@test.local')

    def test_forgot_valid(self):
        r = self.client.post(self.URL, data={'email': 'fp@test.local'}, format='json')
        self.assert_envelope_success(r, 200)

    def test_forgot_unknown_email_still_200(self):
        r = self.client.post(self.URL, data={'email': 'nobody@test.local'}, format='json')
        self.assert_envelope_success(r, 200)


class ResetPasswordTests(MenuMateAPITestCase):
    URL = '/api/v1/users/reset-password/'

    def setUp(self):
        cache.clear()
        self.create_user(email='rp@test.local')

    def test_reset_invalid_code(self):
        r = self.client.post(self.URL, data={
            'email': 'rp@test.local',
            'code': '000000',
            'new_password': 'NewPass456!!',
            'new_password_confirm': 'NewPass456!!',
        }, format='json')
        self.assert_envelope_error(r, 400, reason='verification_code_invalid_or_expired')
