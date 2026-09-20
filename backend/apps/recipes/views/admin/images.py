"""Admin: retsept/ingredient rasmini qidirish va yuklash."""
import os
import uuid

from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from apps.products.utils.image_search import search_images
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


_MAX_UPLOAD_BYTES = 5 * 1024 * 1024
_ALLOWED_MIME_PREFIX = 'image/'
_ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


class ImageSearchAPIView(APIView):
    """GET /admin/recipes/search-image/?query=Manti."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = (request.query_params.get('query') or '').strip()
        if not query:
            raise CustomException(
                "VALIDATION_ERROR",
                status_code=400,
                errors={
                    "detail": "query parameter is required and must not be empty",
                    "field": "query",
                    "reason": "empty_query",
                },
            )
        candidates = search_images(query)
        return CustomResponse.success(
            request=request,
            data={
                'query': query,
                'count': len(candidates),
                'candidates': candidates,
            },
            status_code=200,
        )


class ImageUploadAPIView(APIView):
    """POST /admin/recipes/upload-image/ — multipart 'file' maydoni."""
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser]

    def post(self, request):
        upload = request.FILES.get('file')
        if upload is None:
            raise CustomException(
                "VALIDATION_ERROR",
                status_code=400,
                errors={
                    "detail": "multipart 'file' field is required",
                    "field": "file",
                    "reason": "missing_file",
                },
            )

        if upload.size > _MAX_UPLOAD_BYTES:
            raise CustomException(
                "VALIDATION_ERROR",
                status_code=400,
                errors={
                    "detail": f"file too large: {upload.size} bytes, max {_MAX_UPLOAD_BYTES}",
                    "field": "file",
                    "size": upload.size,
                    "max_size": _MAX_UPLOAD_BYTES,
                    "reason": "file_too_large",
                },
            )

        content_type = (upload.content_type or '').lower()
        if not content_type.startswith(_ALLOWED_MIME_PREFIX):
            raise CustomException(
                "VALIDATION_ERROR",
                status_code=400,
                errors={
                    "detail": f"content-type must be image/*, got {content_type!r}",
                    "field": "file",
                    "content_type": content_type,
                    "reason": "not_an_image",
                },
            )

        ext = os.path.splitext(upload.name or '')[1].lower()
        if ext not in _ALLOWED_EXTENSIONS:
            raise CustomException(
                "VALIDATION_ERROR",
                status_code=400,
                errors={
                    "detail": f"extension {ext!r} is not allowed",
                    "field": "file",
                    "extension": ext,
                    "allowed": sorted(_ALLOWED_EXTENSIONS),
                    "reason": "extension_not_allowed",
                },
            )

        filename = f"uploads/admin/recipes/{uuid.uuid4().hex}{ext}"
        saved = default_storage.save(filename, upload)
        url = default_storage.url(saved)
        if url and not url.startswith(('http://', 'https://')):
            url = request.build_absolute_uri(url)

        return CustomResponse.created(
            request=request,
            data={
                'url': url,
                'filename': saved,
                'size': upload.size,
            },
            status_code=201,
        )
