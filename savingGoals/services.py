from savings.models import Saving
from django.db.models import F
from .models import SavingGoal


def create_saving(user, data):
    # Get the saving goal related to this saving.
    saving_goal = SavingGoal.objects.get(id=data['goal'], user=user)

    # Update the current amount of the saving goal.
    saving_goal.current_amount = F('current_amount') + data['amount']
    saving_goal.save()

    data['user'] = user
    return Saving.objects.create(**data)


def get_all_saving_goals(user):
    return SavingGoal.objects.filter(user=user)


def get_saving_goal(user, goal_id):
    try:
        return SavingGoal.objects.get(id=goal_id, user=user)
    except SavingGoal.DoesNotExist:
        return None


def update_saving_goal(user, goal_id, data):
    goal = get_saving_goal(user, goal_id)
    if goal:
        for attr, value in data.items():
            setattr(goal, attr, value)
        goal.save()
        return goal
    return None


def delete_saving_goal(user, goal_id):
    goal = get_saving_goal(user, goal_id)
    if goal:
        goal.delete()
        return True
    return False
