"""Menu: yaratish, ko'rish, meal items qo'shish, olib tashlash."""
from datetime import date, timedelta

from django.core.cache import cache

from apps.menu.models.menu import Menu, MenuMealItem
from apps.recipes.models.recipes import Recipe
from apps.shared.tests.utils import MenuMateAPITestCase


class MenuFlowTests(MenuMateAPITestCase):
    LIST_URL = '/api/v1/menu/'
    fixtures = ['allergen_tags', 'ingredients', 'recipes', 'recipe_ingredients', 'recipe_steps']

    def setUp(self):
        cache.clear()
        self.user, _ = self.create_and_login(email='menu@test.local')
        self.client.post('/api/v1/family/', data={
            'family_name': 'X', 'city': 'Y',
        }, format='json')
        self.client.post('/api/v1/family/members/', data={
            'name': 'Ali', 'age': 30, 'gender': 'MALE',
        }, format='json')

    def test_create_menu_valid(self):
        r = self.client.post(self.LIST_URL, data={
            'start_date': str(date.today() + timedelta(days=1)),
            'duration': 'WEEKLY',
        }, format='json')
        body = self.assert_envelope_success(r, 201)
        self.assertIn('days', body['data'])
        self.assertGreater(len(body['data']['days']), 0)

    def test_create_menu_without_family(self):
        self.client.credentials()
        user2, _ = self.create_and_login(email='alone@test.local')
        r = self.client.post(self.LIST_URL, data={
            'start_date': str(date.today() + timedelta(days=1)),
            'duration': 'WEEKLY',
        }, format='json')
        self.assert_envelope_error(r, 404, reason='user_has_no_family')

    def test_create_menu_no_members(self):
        self.client.credentials()
        user2, _ = self.create_and_login(email='fam@test.local')
        self.client.post('/api/v1/family/', data={
            'family_name': 'Q', 'city': 'W',
        }, format='json')
        r = self.client.post(self.LIST_URL, data={
            'start_date': str(date.today() + timedelta(days=1)),
            'duration': 'WEEKLY',
        }, format='json')
        self.assert_envelope_error(r, 400, reason='family_has_no_members')

    def test_get_menu_404(self):
        r = self.client.get(f'{self.LIST_URL}999999/')
        self.assert_envelope_error(r, 404, reason='menu_not_found_or_forbidden')

    def test_add_meal_item_valid(self):
        r = self.client.post(self.LIST_URL, data={
            'start_date': str(date.today() + timedelta(days=1)),
            'duration': 'WEEKLY',
        }, format='json')
        menu = r.json()['data']
        meal_id = menu['days'][0]['meals'][0]['id']
        recipe_id = Recipe.objects.first().pk

        r = self.client.post(f'/api/v1/menu/meals/{meal_id}/items/', data={
            'recipe_id': recipe_id, 'category': 'MAIN',
        }, format='json')
        self.assert_envelope_success(r, 201)
        self.assertTrue(MenuMealItem.objects.filter(meal_id=meal_id).exists())

    def test_add_meal_item_invalid_recipe(self):
        r = self.client.post(self.LIST_URL, data={
            'start_date': str(date.today() + timedelta(days=1)),
            'duration': 'WEEKLY',
        }, format='json')
        meal_id = r.json()['data']['days'][0]['meals'][0]['id']

        r = self.client.post(f'/api/v1/menu/meals/{meal_id}/items/', data={
            'recipe_id': 999999, 'category': 'MAIN',
        }, format='json')
        self.assert_envelope_error(r, 400, reason='unknown_recipe_id')

    def test_recommendations_invalid_category(self):
        r = self.client.post(self.LIST_URL, data={
            'start_date': str(date.today() + timedelta(days=1)),
            'duration': 'WEEKLY',
        }, format='json')
        meal_id = r.json()['data']['days'][0]['meals'][0]['id']

        r = self.client.get(f'/api/v1/menu/meals/{meal_id}/recommendations/?category=BADCAT')
        self.assert_envelope_error(r, 400, reason='invalid_meal_category')

    def test_delete_menu(self):
        r = self.client.post(self.LIST_URL, data={
            'start_date': str(date.today() + timedelta(days=1)),
            'duration': 'WEEKLY',
        }, format='json')
        menu_id = r.json()['data']['id']
        r = self.client.delete(f'{self.LIST_URL}{menu_id}/')
        self.assert_envelope_success(r, 200)
        self.assertFalse(Menu.objects.filter(pk=menu_id).exists())
