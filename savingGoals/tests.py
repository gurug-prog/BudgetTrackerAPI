from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from savingGoals import services
from .models import SavingGoal


class SavingGoalServiceTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='test')
        cls.saving_goal = SavingGoal.objects.create(
            user=cls.user, name='Test Goal', target_amount=500.0)

    def test_create_saving_goal(self):
        data = {'name': 'Test Goal 2', 'target_amount': 1000.0}
        goal = services.create_saving_goal(self.user, data)
        self.assertIsInstance(goal, SavingGoal)

    def test_get_all_saving_goals(self):
        goals = services.get_all_saving_goals(self.user)
        self.assertEqual(goals.count(), 1)

    def test_get_saving_goal(self):
        goal = services.get_saving_goal(self.user, self.saving_goal.id)
        self.assertIsInstance(goal, SavingGoal)

    def test_update_saving_goal(self):
        data = {'target_amount': 800.0}
        goal = services.update_saving_goal(
            self.user, self.saving_goal.id, data)
        self.assertEqual(goal.target_amount, 800.0)

    def test_delete_saving_goal(self):
        result = services.delete_saving_goal(self.user, self.saving_goal.id)
        self.assertTrue(result)


class SavingGoalViewTest(APITestCase):
    client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='test')
        cls.saving_goal = SavingGoal.objects.create(
            user=cls.user, name='Test Goal', target_amount=500.0)
        cls.token = 'Bearer '  # Here should be the token got from JWT

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_get_all_saving_goals(self):
        response = self.client.get(reverse('saving_goals-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_saving_goal(self):
        response = self.client.get(
            reverse('saving_goals-detail', kwargs={'pk': self.saving_goal.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_saving_goal(self):
        data = {'name': 'Test Goal 2', 'target_amount': 1000.0}
        response = self.client.post(reverse('saving_goals-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_saving_goal(self):
        data = {'target_amount': 800.0}
        response = self.client.put(
            reverse('saving_goals-detail', kwargs={'pk': self.saving_goal.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_saving_goal(self):
        response = self.client.delete(
            reverse('saving_goals-detail', kwargs={'pk': self.saving_goal.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
