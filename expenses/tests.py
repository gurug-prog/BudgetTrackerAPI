from django.contrib.auth.models import User
from django.test import TestCase
from .models import Expense, Category
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .services import create_expense, get_all_expenses, get_expense, update_expense, delete_expense


class ExpenseServicesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.category = Category.objects.create(
            name='Test', color='#000', user=self.user)
        self.expense = Expense.objects.create(
            user=self.user, date='2023-06-08', amount=200.0, category=self.category)

    def test_create_expense(self):
        data = {'date': '2023-06-09', 'amount': 150.0,
                'category': self.category.id}
        expense = create_expense(self.user, data)
        self.assertEqual(expense.amount, 150.0)

    def test_get_all_expenses(self):
        expenses = get_all_expenses(self.user)
        self.assertEqual(len(expenses), 1)

    def test_get_expense(self):
        expense = get_expense(self.user, self.expense.id)
        self.assertEqual(expense, self.expense)

    def test_update_expense(self):
        data = {'date': '2023-06-10', 'amount': 300.0,
                'category': self.category.id}
        expense = update_expense(self.user, self.expense.id, data)
        self.assertEqual(expense.amount, 300.0)

    def test_delete_expense(self):
        result = delete_expense(self.user, self.expense.id)
        self.assertEqual(result, True)


class ExpenseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_expense(user, category):
        Expense.objects.create(user=user, date='2023-06-08',
                               amount=200.0, category=category)

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.category = Category.objects.create(
            name='Test', color='#000', user=self.user)
        self.create_expense(self.user, self.category)
        self.token = 'Bearer '  # Here should be the token got from JWT
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_get_all_expenses(self):
        response = self.client.get(reverse('expenses-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_expense(self):
        expense = Expense.objects.first()
        response = self.client.get(
            reverse('expenses-detail', kwargs={'pk': expense.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_expense(self):
        data = {'date': '2023-06-09', 'amount': 300.0,
                'category': self.category.id}
        response = self.client.post(reverse('expenses-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_expense(self):
        expense = Expense.objects.first()
        data = {'date': '2023-06-10', 'amount': 400.0,
                'category': self.category.id}
        response = self.client.put(
            reverse('expenses-detail', kwargs={'pk': expense.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_expense(self):
        expense = Expense.objects.first()
        response = self.client.delete(
            reverse('expenses-detail', kwargs={'pk': expense.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
