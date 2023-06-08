from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from savings import services
from .models import Saving, SavingGoal


class SavingServiceTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='test')
        cls.saving_goal = SavingGoal.objects.create(
            user=cls.user, name='Test Goal', target_amount=500.0)
        cls.saving = Saving.objects.create(
            user=cls.user, goal=cls.saving_goal, year=2023, month=6, amount=200.0)

    def test_create_saving(self):
        data = {'goal': self.saving_goal.id,
                'year': 2023, 'month': 7, 'amount': 300.0}
        saving = services.create_saving(self.user, data)
        self.assertIsInstance(saving, Saving)

    def test_get_all_savings(self):
        savings = services.get_all_savings(self.user)
        self.assertEqual(savings.count(), 1)

    def test_get_saving(self):
        saving = services.get_saving(self.user, self.saving.id)
        self.assertIsInstance(saving, Saving)

    def test_update_saving(self):
        data = {'amount': 400.0}
        saving = services.update_saving(self.user, self.saving.id, data)
        self.assertEqual(saving.amount, 400.0)

    def test_delete_saving(self):
        result = services.delete_saving(self.user, self.saving.id)
        self.assertTrue(result)


class SavingViewTest(APITestCase):
    client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='test')
        cls.saving_goal = SavingGoal.objects.create(
            user=cls.user, name='Test Goal', target_amount=500.0)
        cls.saving = Saving.objects.create(
            user=cls.user, goal=cls.saving_goal, year=2023, month=6, amount=200.0)
        cls.token = 'Bearer '  # Here should be the token got from JWT

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_get_all_savings(self):
        response = self.client.get(reverse('savings-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_saving(self):
        response = self.client.get(
            reverse('savings-detail', kwargs={'pk': self.saving.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_saving(self):
        data = {'goal': self.saving_goal.id,
                'year': 2023, 'month': 7, 'amount': 300.0}
        response = self.client.post(reverse('savings-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_saving(self):
        data = {'amount': 400.0}
        response = self.client.put(
            reverse('savings-detail', kwargs={'pk': self.saving.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_saving(self):
        response = self.client.delete(
            reverse('savings-detail', kwargs={'pk': self.saving.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
