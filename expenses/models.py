from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from categories.models import Category


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    # Adjust max_digits and decimal_places as per your requirements
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
