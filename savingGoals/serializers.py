from rest_framework import serializers
from .models import SavingGoal

class SavingGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingGoal
        fields = ['id', 'user', 'name', 'target_amount', 'current_amount']

    # Ensure the user field is read-only
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
