from rest_framework import serializers

from savingGoals.models import SavingGoal
from .models import Saving


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = ['id', 'user', 'goal', 'year', 'month', 'amount']

    # Ensure the user field is read-only
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # Convert the goal field to just use the ID
    goal = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=SavingGoal.objects.all())
