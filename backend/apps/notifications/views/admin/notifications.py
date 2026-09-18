"""Admin: Bildirishnomalar va broadcast."""
from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView

from apps.devices.models.device import Device
from apps.notifications.models.notifications import Notification
from apps.notifications.serializers.admin import (
    BroadcastNotificationSerializer,
    NotificationAdminSerializer,
)
from apps.shared.permissions import IsAdminUser
from apps.shared.throttling import BroadcastThrottle
from apps.shared.utils.custom_response import CustomResponse
from apps.users.models.users import User


class NotificationsAdminListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Notification.objects.select_related('user').order_by('-created_at')[:200]
        return CustomResponse.success(
            request=request,
            data=NotificationAdminSerializer(qs, many=True).data,
        )


class BroadcastAPIView(APIView):
    """POST /admin/notifications/broadcast/ — barcha faol foydalanuvchilarga xabar.

    Flow:
      1. Serializer validate qiladi.
      2. Transaction ichida har foydalanuvchi uchun `Notification` yaratamiz.
      3. `post_save` signal + `transaction.on_commit` — Celery orqali push.
      4. Javobda nechta foydalanuvchi va nechta qurilma qamrab olinganini
         qaytaramiz (push loyihasining ko'rinish tomoni).
    """
    permission_classes = [IsAdminUser]
    throttle_classes = [BroadcastThrottle]

    def post(self, request):
        serializer = BroadcastNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        now = timezone.now()
        users = list(
            User.objects.filter(
                is_active=True, is_deleted=False, is_push_enabled=True,
            ).values_list('id', flat=True)
        )

        devices_reached = Device.objects.filter(
            user_id__in=users, is_active=True,
        ).exclude(fcm_token='').count()

        with transaction.atomic():
            Notification.objects.bulk_create([
                Notification(
                    user_id=uid,
                    kind=data['kind'],
                    title=data['title'],
                    body=data['body'],
                    image_url=data.get('image_url', '') or '',
                    sent_at=None,  # signal yuborgach yozadi
                )
                for uid in users
            ])

        # NOTE: `bulk_create` `post_save` signal chaqirmaydi. Push yuborishni
        # to'g'ridan-to'g'ri o'zimiz olib boramiz — bir marta multicast.
        _enqueue_broadcast_push(
            title=data['title'],
            body=data['body'],
            image_url=data.get('image_url', '') or '',
            kind=data['kind'],
            user_ids=users,
        )

        return CustomResponse.created(
            request=request,
            data={
                'sent_count': len(users),
                'devices_reached': devices_reached,
                'sent_at': now.isoformat(),
            },
        )


def _enqueue_broadcast_push(
    *,
    title: str,
    body: str,
    image_url: str,
    kind: str,
    user_ids: list[int],
) -> None:
    """Broadcast push — bir vaqtda 500 tagacha token'ga."""
    if not user_ids:
        return

    from apps.notifications.tasks import send_push_multicast

    tokens = list(
        Device.objects.filter(user_id__in=user_ids, is_active=True)
        .exclude(fcm_token='')
        .values_list('fcm_token', flat=True)
    )
    if not tokens:
        return

    # Transaction commit'dan keyin ishga tushiramiz
    transaction.on_commit(
        lambda: send_push_multicast.delay(
            tokens,
            title=title,
            body=body,
            data={'kind': kind, 'type': 'broadcast'},
            image_url=image_url,
        )
    )
