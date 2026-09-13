from modeltranslation.translator import TranslationOptions, register

from apps.notifications.models.notifications import Holiday


@register(Holiday)
class HolidayTranslation(TranslationOptions):
    fields = ('name', 'description')
