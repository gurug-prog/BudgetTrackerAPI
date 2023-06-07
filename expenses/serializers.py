from rest_framework import serializers

from categories.models import Category
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'date', 'amount', 'category']

    # Ensure the user field is read-only
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # Convert the category field to just use the ID
    category = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Category.objects.all())
