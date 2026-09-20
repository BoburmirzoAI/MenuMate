"""CustomResponse va CustomException envelope va status kodlari."""
from django.test import RequestFactory
from django.test import TestCase

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.exceptions.handler import custom_exception_handler
from apps.shared.utils.custom_response import CustomResponse


class CustomResponseTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')

    def test_success_returns_200(self):
        r = CustomResponse.success(request=self.request, data={'x': 1})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.data['success'])
        self.assertEqual(r.data['data'], {'x': 1})

    def test_success_with_explicit_status(self):
        r = CustomResponse.success(request=self.request, status_code=204)
        self.assertEqual(r.status_code, 204)

    def test_created_returns_201(self):
        r = CustomResponse.created(request=self.request, data={'ok': True})
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.data['success'])

    def test_created_with_explicit_status_code_no_conflict(self):
        r = CustomResponse.created(request=self.request, data={}, status_code=201)
        self.assertEqual(r.status_code, 201)

    def test_error_envelope(self):
        r = CustomResponse.error(
            message_key='NOT_FOUND', request=self.request,
            errors={'detail': 'x', 'reason': 'y'},
        )
        self.assertEqual(r.status_code, 404)
        self.assertFalse(r.data['success'])
        self.assertIn('id', r.data)
        self.assertIn('errors', r.data)
        self.assertEqual(r.data['errors']['reason'], 'y')


class CustomExceptionTests(TestCase):
    def _handle(self, exc: CustomException):
        return custom_exception_handler(exc, {'request': RequestFactory().get('/')})

    def test_exception_with_status_code(self):
        exc = CustomException('NOT_FOUND', status_code=404, errors={
            'detail': 'x', 'reason': 'r',
        })
        r = self._handle(exc)
        self.assertEqual(r.status_code, 404)
        self.assertFalse(r.data['success'])
        self.assertEqual(r.data['errors']['reason'], 'r')

    def test_exception_default_status_from_message_key(self):
        exc = CustomException('VALIDATION_ERROR')
        r = self._handle(exc)
        self.assertEqual(r.status_code, 400)

    def test_exception_carries_errors_through(self):
        exc = CustomException(
            'MENU_NOT_FOUND',
            status_code=404,
            errors={
                'detail': 'Menu 42 not found for user 5',
                'menu_id': 42, 'user_id': 5, 'reason': 'menu_not_found',
            },
        )
        r = self._handle(exc)
        self.assertEqual(r.data['errors']['menu_id'], 42)
        self.assertEqual(r.data['errors']['reason'], 'menu_not_found')
