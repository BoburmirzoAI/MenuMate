from django.db import models

from apps.shared.models import BaseModel


class FamilyProfile(BaseModel):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='family',
    )
    family_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, help_text="Ob-havo API uchun shahar nomi")

    class Meta:
        db_table = 'family_profile'

    def __str__(self):
        return f"{self.family_name} ({self.user.email})"


class HealthCondition(BaseModel):
    """
    Reference table of health conditions (allergy, diabetes, etc).
    Populated via fixture.
    """

    class Category(models.TextChoices):
        ALLERGY = 'ALLERGY', 'Allergiya'
        DIABETES = 'DIABETES', 'Diabet'
        HEART = 'HEART', 'Yurak kasalligi'
        OBESITY = 'OBESITY', 'Semizlik'
        OTHER = 'OTHER', 'Boshqa'

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'family_health_condition'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class FamilyMember(BaseModel):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Erkak'
        FEMALE = 'FEMALE', 'Ayol'

    family = models.ForeignKey(
        FamilyProfile, on_delete=models.CASCADE, related_name='members'
    )
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, choices=Gender.choices)

    liked_recipes = models.ManyToManyField(
        'recipes.Recipe', related_name='liked_by', blank=True
    )
    disliked_recipes = models.ManyToManyField(
        'recipes.Recipe', related_name='disliked_by', blank=True
    )
    health_conditions = models.ManyToManyField(
        HealthCondition, related_name='members', blank=True
    )
    allergen_ingredients = models.ManyToManyField(
        'recipes.Ingredient',
        related_name='allergic_members',
        blank=True,
        help_text="Ingredientlarga allergiya (dukkakli, sut, tuxum va h.k.)",
    )

    class Meta:
        db_table = 'family_member'

    def __str__(self):
        return f"{self.name} ({self.family.family_name})"
