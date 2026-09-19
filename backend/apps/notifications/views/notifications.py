"""
Notifications views.

GET  /notifications/holidays/          — barcha bayramlar
GET  /notifications/holidays/upcoming/ — keyingi 30 kunda kelayotgan bayramlar
GET  /notifications/                    — user notification'lari (ro'yxat)
PATCH /notifications/<id>/read/         — o'qildi belgilash
POST /notifications/mark-all-read/     — hammasi o'qildi
"""
from datetime import date, timedelta

from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.notifications.models.notifications import Holiday, Notification
from apps.notifications.serializers.notifications import (
    HolidaySerializer,
    NotificationSerializer,
)
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.utils.custom_response import CustomResponse


class HolidayListAPIView(ListAPIView):
    """GET /notifications/holidays/"""
    permission_classes = [IsAuthenticated]
    serializer_class = HolidaySerializer
    queryset = Holiday.objects.all()
    pagination_class = None

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return CustomResponse.success(request=request, data=serializer.data, status_code=200)


class UpcomingHolidaysAPIView(APIView):
    """
    GET /notifications/holidays/upcoming/?days=30
    Keyingi N kun ichida kelayotgan bayramlar (sana bo'yicha tartiblanadi).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            days = int(request.query_params.get('days', 30))
        except ValueError:
            days = 30
        days = max(1, min(days, 365))

        today = date.today()
        end_date = today + timedelta(days=days)

        upcoming = []
        for holiday in Holiday.objects.all():
            try:
                this_year = date(today.year, holiday.month, holiday.day)
            except ValueError:
                continue
            check_date = this_year if this_year >= today else date(
                today.year + 1, holiday.month, holiday.day,
            )
            if today <= check_date <= end_date:
                data = HolidaySerializer(holiday).data
                data['upcoming_date'] = check_date.isoformat()
                data['days_until'] = (check_date - today).days
                upcoming.append(data)

        upcoming.sort(key=lambda x: x['days_until'])
        return CustomResponse.success(request=request, data=upcoming, status_code=200)


class NotificationListAPIView(ListAPIView):
    """GET /notifications/ — user'ning notification'lari."""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user)
        unread_only = self.request.query_params.get('unread', '').lower() in ('true', '1')
        if unread_only:
            qs = qs.filter(is_read=False)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return CustomResponse.success(
                request=request,
                data=self.paginator.get_paginated_data(serializer.data),
                status_code=200,
            )
        serializer = self.get_serializer(qs, many=True)
        return CustomResponse.success(request=request, data=serializer.data, status_code=200)


class MarkNotificationReadAPIView(APIView):
    """PATCH /notifications/<id>/read/"""
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        notif = Notification.objects.filter(
            id=notification_id, user=request.user,
        ).first()
        if not notif:
            raise CustomException(
                "NOTIFICATION_NOT_FOUND",
                status_code=404,
                errors={
                    "detail": f"Notification id={notification_id} not found for user_id={request.user.pk}",
                    "notification_id": notification_id,
                    "user_id": request.user.pk,
                    "reason": "notification_not_found_or_forbidden",
                },
            )

        if not notif.is_read:
            notif.is_read = True
            notif.save(update_fields=['is_read'])

        return CustomResponse.success(
            request=request,
            data=NotificationSerializer(notif).data,
            message_key="UPDATED",
            status_code=200,
        )


class MarkAllNotificationsReadAPIView(APIView):
    """POST /notifications/mark-all-read/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        count = Notification.objects.filter(
            user=request.user, is_read=False,
        ).update(is_read=True)
        return CustomResponse.success(
            request=request,
            data={'marked_count': count},
            message_key="ALL_NOTIFICATIONS_READ",
            status_code=200,
        )
