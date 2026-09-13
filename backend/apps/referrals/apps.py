from django.apps import AppConfig


class ReferralsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.referrals'

    def ready(self):
        from apps.referrals import signals  # noqa: F401
