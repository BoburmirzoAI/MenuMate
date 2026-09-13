from modeltranslation.translator import TranslationOptions, register

from apps.family.models.family import HealthCondition


@register(HealthCondition)
class HealthConditionTranslation(TranslationOptions):
    fields = ('name', 'description')
