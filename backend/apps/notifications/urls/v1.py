from django.urls import path

from apps.notifications.views.notifications import (
    HolidayListAPIView,
    MarkAllNotificationsReadAPIView,
    MarkNotificationReadAPIView,
    NotificationListAPIView,
    UpcomingHolidaysAPIView,
)

app_name = 'notifications'

urlpatterns = [
    # --- Holidays ---
    path('holidays/', HolidayListAPIView.as_view(), name='holidays'),
    path('holidays/upcoming/', UpcomingHolidaysAPIView.as_view(), name='holidays-upcoming'),

    # --- User notifications ---
    path('', NotificationListAPIView.as_view(), name='list'),
    path('mark-all-read/', MarkAllNotificationsReadAPIView.as_view(), name='mark-all-read'),
    path('<int:notification_id>/read/',
         MarkNotificationReadAPIView.as_view(), name='mark-read'),
]
