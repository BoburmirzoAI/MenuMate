"""Admin: retsept rasm qidiruv va yuklash."""
import struct
import zlib
from unittest.mock import patch

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.shared.tests.utils import MenuMateAPITestCase


def _make_png() -> bytes:
    def _chunk(t: bytes, d: bytes) -> bytes:
        crc = zlib.crc32(t + d) & 0xffffffff
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', crc)

    signature = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', 4, 4, 8, 2, 0, 0, 0)
    raw = b''.join(b'\x00' + b'\xff\x00\x00' * 4 for _ in range(4))
    idat = zlib.compress(raw)
    return signature + _chunk(b'IHDR', ihdr) + _chunk(b'IDAT', idat) + _chunk(b'IEND', b'')


class ImageSearchTests(MenuMateAPITestCase):
    URL = '/api/v1/admin/recipes/search-image/'

    def setUp(self):
        cache.clear()
        self.create_and_login(
            email='admin_img@test.local', is_staff=True, is_superuser=True,
        )

    def test_empty_query_returns_400(self):
        r = self.client.get(f'{self.URL}?query=')
        self.assert_envelope_error(r, 400, reason='empty_query')

    def test_no_auth(self):
        self.client.credentials()
        r = self.client.get(f'{self.URL}?query=test')
        self.assertIn(r.status_code, (401, 403))

    @patch('apps.products.utils.image_search.requests.get')
    def test_query_returns_candidates(self, mock_get):
        class R:
            status_code = 200
            def json(self):
                return {
                    'title': 'Test',
                    'thumbnail': {'source': 'https://x/thumb.jpg'},
                    'originalimage': {'source': 'https://x/orig.jpg'},
                }
        mock_get.return_value = R()
        r = self.client.get(f'{self.URL}?query=Manti')
        body = self.assert_envelope_success(r, 200)
        self.assertIn('candidates', body['data'])
        self.assertGreater(body['data']['count'], 0)


class ImageUploadTests(MenuMateAPITestCase):
    URL = '/api/v1/admin/recipes/upload-image/'

    def setUp(self):
        cache.clear()
        self.create_and_login(
            email='admin_up@test.local', is_staff=True, is_superuser=True,
        )

    def test_upload_valid_png(self):
        png = _make_png()
        upload = SimpleUploadedFile('test.png', png, content_type='image/png')
        r = self.client.post(self.URL, {'file': upload}, format='multipart')
        body = self.assert_envelope_success(r, 201)
        self.assertIn('url', body['data'])

    def test_upload_text_rejected(self):
        upload = SimpleUploadedFile('bad.txt', b'text', content_type='text/plain')
        r = self.client.post(self.URL, {'file': upload}, format='multipart')
        self.assert_envelope_error(r, 400, reason='not_an_image')

    def test_upload_svg_rejected(self):
        upload = SimpleUploadedFile('e.svg', b'<svg/>', content_type='image/svg+xml')
        r = self.client.post(self.URL, {'file': upload}, format='multipart')
        self.assert_envelope_error(r, 400, reason='extension_not_allowed')

    def test_upload_too_large(self):
        big = b'\x89PNG' + b'\x00' * (6 * 1024 * 1024)
        upload = SimpleUploadedFile('big.png', big, content_type='image/png')
        r = self.client.post(self.URL, {'file': upload}, format='multipart')
        self.assert_envelope_error(r, 400, reason='file_too_large')

    def test_missing_file(self):
        r = self.client.post(self.URL, {}, format='multipart')
        self.assert_envelope_error(r, 400, reason='missing_file')

    def test_no_auth(self):
        self.client.credentials()
        r = self.client.post(self.URL, {}, format='multipart')
        self.assertIn(r.status_code, (401, 403))
