"""test for the ingredients API"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Create and return an ingredient detail URL."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@example.com', password='testpass123'):
    """create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class PublicIngredientApiTest(TestCase):
    """Test Unauthenticated Api requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """test auth required for retrieving ingredients"""

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """Test Authenticated Api requests"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """test retrieving a list of ingredients"""
        Ingredient.objects.create(
            user=self.user,
            name='Spinach'
        )
        Ingredient.objects.create(
            user=self.user,
            name='Kales'
        )

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user"""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123'
        )

        Ingredient.objects.create(
            user=other_user,
            name='Spinach'
        )
        Ingredient.objects.create(
            user=self.user,
            name='Kales'
        )

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.filter(user=self.user)
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_ingredients(self):
        """test updating an Ingredient"""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='Kales'
        )

        payload = {'name': 'managu'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """testing deleting ingredients"""
        ingredient = Ingredient.objects.create(user=self.user, name='royco')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())
