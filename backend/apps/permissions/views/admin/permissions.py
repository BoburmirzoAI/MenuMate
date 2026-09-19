"""Admin: Rollar, permissionlar va endpointlar CRUD."""
from django.db.models import Q
from rest_framework import serializers
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


class _PermissionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'codename', 'description', 'parent']


class PermissionsAdminListAPIView(APIView):
    """GET/POST /admin/permissions/permissions/"""
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

    def post(self, request):
        serializer = _PermissionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        perm = serializer.save()
        return CustomResponse.created(
            request=request,
            data=PermissionAdminSerializer(perm).data,
        )


class PermissionsAdminDetailAPIView(APIView):
    """GET/PATCH/DELETE /admin/permissions/permissions/<id>/"""
    permission_classes = [IsAdminUser]

    def _get(self, perm_id):
        perm = Permission.objects.filter(id=perm_id).first()
        if not perm:
            raise CustomException("NOT_FOUND")
        return perm

    def get(self, request, perm_id):
        return CustomResponse.success(
            request=request,
            data=PermissionAdminSerializer(self._get(perm_id)).data,
        )

    def patch(self, request, perm_id):
        perm = self._get(perm_id)
        serializer = _PermissionWriteSerializer(perm, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=PermissionAdminSerializer(perm).data,
        )

    def delete(self, request, perm_id):
        self._get(perm_id).delete()
        return CustomResponse.success(request=request, message_key="DELETED")


class _EndpointWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ['access_type', 'permission', 'is_active', 'name', 'description']


class EndpointsAdminListAPIView(APIView):
    """GET /admin/permissions/endpoints/"""
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


class EndpointsAdminDetailAPIView(APIView):
    """GET/PATCH /admin/permissions/endpoints/<id>/ — Endpoint faqat sozlashda tahrirlanadi."""
    permission_classes = [IsAdminUser]

    def _get(self, endpoint_id):
        ep = Endpoint.objects.filter(id=endpoint_id).first()
        if not ep:
            raise CustomException("NOT_FOUND")
        return ep

    def get(self, request, endpoint_id):
        return CustomResponse.success(
            request=request,
            data=EndpointAdminSerializer(self._get(endpoint_id)).data,
        )

    def patch(self, request, endpoint_id):
        ep = self._get(endpoint_id)
        serializer = _EndpointWriteSerializer(ep, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            request=request,
            data=EndpointAdminSerializer(ep).data,
        )
