from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from categories import services
from .models import Category


class CategoryServiceTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name='Test Category', description='Test Description')

    def test_create_category(self):
        data = {'name': 'Test Category 2', 'description': 'Test Description 2'}
        category = services.create_category(data)
        self.assertIsInstance(category, Category)

    def test_get_all_categories(self):
        categories = services.get_all_categories()
        self.assertEqual(categories.count(), 1)

    def test_get_category(self):
        category = services.get_category(self.category.id)
        self.assertIsInstance(category, Category)

    def test_update_category(self):
        data = {'description': 'Updated Description'}
        category = services.update_category(self.category.id, data)
        self.assertEqual(category.description, 'Updated Description')

    def test_delete_category(self):
        result = services.delete_category(self.category.id)
        self.assertTrue(result)


class CategoryViewTest(APITestCase):
    client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='test')
        cls.category = Category.objects.create(
            name='Test Category', description='Test Description')
        cls.token = 'Bearer '  # Here should be the token got from JWT

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_get_all_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category(self):
        response = self.client.get(
            reverse('category-detail', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        data = {'name': 'Test Category 2', 'description': 'Test Description 2'}
        response = self.client.post(reverse('category-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category(self):
        data = {'description': 'Updated Description'}
        response = self.client.put(
            reverse('category-detail', kwargs={'pk': self.category.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        response = self.client.delete(
            reverse('category-detail', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
