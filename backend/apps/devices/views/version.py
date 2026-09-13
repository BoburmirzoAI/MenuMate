from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.shared.utils.custom_response import CustomResponse
from apps.devices.models.app_version import VersionPolicy
from apps.devices.serializers.version import VersionCheckSerializer


class VersionCheckAPIView(APIView):
    """
    Mobile ilova app start'da chaqiradi.
    Response.status:
      - OK                   — ilova ishlashi mumkin
      - UPDATE_RECOMMENDED   — yangi versiya bor, foydalanuvchi tanlaydi
      - UPDATE_REQUIRED      — force update, ilovaga kirish taqiqlanadi
    """
    permission_classes = [AllowAny]
    serializer_class = VersionCheckSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        platform = serializer.validated_data['platform']
        app_version = serializer.validated_data['app_version']
        os_version = serializer.validated_data.get('os_version', '')

        policy = VersionPolicy.objects.filter(platform=platform).first()
        if not policy:
            # Policy hali sozlanmagan — barcha versiyalar ruxsat etiladi
            return CustomResponse.success(
                request=request,
                data={
                    'status': 'OK',
                    'reason': None,
                    'current_version': app_version,
                    'min_required_version': app_version,
                    'store_url': '',
                },
            )

        result = policy.check_version(client_version=app_version, os_version=os_version)

        lang_map = {
            'uz': policy.message_uz,
            'ru': policy.message_ru,
            'en': policy.message_en,
        }
        accept_lang = (request.headers.get('Accept-Language') or 'uz').split(',')[0].split('-')[0]
        result['message'] = lang_map.get(accept_lang) or policy.message_uz or ''

        return CustomResponse.success(request=request, data=result)
