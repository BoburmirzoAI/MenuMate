"""Test yordamchi utilities — hamma test fayllar uchun umumiy."""
from rest_framework.test import APITestCase

from apps.users.models.users import User


class MenuMateAPITestCase(APITestCase):
    """Standart envelope va tokenlash uchun yordamchi metodlar bilan APITestCase."""

    def assert_envelope_success(self, response, status_code: int = 200) -> dict:
        self.assertEqual(response.status_code, status_code)
        body = response.json()
        self.assertTrue(body.get('success'), f'success!=True: {body}')
        self.assertIn('id', body)
        self.assertIn('message', body)
        return body

    def assert_envelope_error(
        self,
        response,
        status_code: int,
        reason: str | None = None,
    ) -> dict:
        """Xato javob — envelope tekshiruvi. reason berilsa custom format ham tekshiriladi."""
        self.assertEqual(response.status_code, status_code)
        body = response.json()
        self.assertFalse(body.get('success'), f'success!=False: {body}')
        self.assertIn('id', body)
        self.assertIn('message', body)
        self.assertIn('errors', body)
        if reason is not None:
            errors = body.get('errors') or {}
            self.assertIn('detail', errors, f'errors.detail yo\'q: {errors}')
            self.assertIn('reason', errors, f'errors.reason yo\'q: {errors}')
            self.assertEqual(errors.get('reason'), reason)
        return body

    def create_user(
        self,
        email: str = 'user@test.local',
        password: str = 'TestPass123!!',
        **kwargs,
    ) -> User:
        return User.objects.create_user(email=email, password=password, **kwargs)

    def login(self, email: str, password: str) -> str:
        r = self.client.post(
            '/api/v1/users/login/',
            data={'email': email, 'password': password},
            format='json',
        )
        assert r.status_code == 200, r.content
        return r.json()['data']['tokens']['access']

    def auth(self, token: str) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def create_and_login(self, **kwargs) -> tuple[User, str]:
        user = self.create_user(**kwargs)
        token = self.login(user.email, kwargs.get('password', 'TestPass123!!'))
        self.auth(token)
        return user, token
