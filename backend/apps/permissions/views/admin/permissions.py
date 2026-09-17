"""Admin: Rollar, permissionlar va endpointlar."""
from django.db.models import Q
from rest_framework.views import APIView

from apps.permissions.models.permissions import Endpoint, Permission, Role
from apps.permissions.serializers.admin import (
    EndpointAdminSerializer,
    PermissionAdminSerializer,
    RoleAdminSerializer,
    RoleAdminUpdateSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.permissions import IsAdminUser
from apps.shared.utils.custom_response import CustomResponse


class RolesAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Role.objects.prefetch_related('permissions').all()
        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(name__icontains=search)
        return CustomResponse.success(
            request=request,
            data=RoleAdminSerializer(qs, many=True).data,
        )

    def post(self, request):
        serializer = RoleAdminUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()
        return CustomResponse.created(
            request=request,
            data=RoleAdminSerializer(role).data,
        )


class RolesAdminDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def _get(self, role_id):
        r = Role.objects.filter(id=role_id).first()
        if not r:
            raise CustomException("NOT_FOUND")
        return r

    def get(self, request, role_id):
        return CustomResponse.success(
            request=request,
            data=RoleAdminSerializer(self._get(role_id)).data,
        )

    def patch(self, request, role_id):
        role = self._get(role_id)
        serializer = RoleAdminUpdateSerializer(role, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=RoleAdminSerializer(role).data,
        )

    def delete(self, request, role_id):
        self._get(role_id).delete()
        return CustomResponse.success(request=request, message_key="DELETED")


class PermissionsAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Permission.objects.prefetch_related('roles').all()
        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(codename__icontains=search))
        return CustomResponse.success(
            request=request,
            data=PermissionAdminSerializer(qs, many=True).data,
        )


class EndpointsAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Endpoint.objects.select_related('permission').all()
        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(Q(path__icontains=search) | Q(method__icontains=search))
        access_type = request.query_params.get('access_type')
        if access_type in ('public', 'authenticated', 'permission'):
            qs = qs.filter(access_type=access_type)
        return CustomResponse.success(
            request=request,
            data=EndpointAdminSerializer(qs, many=True).data,
        )
