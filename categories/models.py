from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    hex_color = models.CharField(max_length=7)  # For storing Hex color codes

    class Meta:
        verbose_name_plural = "Categories"
