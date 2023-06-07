from .models import Expense

def create_expense(user, data):
    data['user'] = user
    return Expense.objects.create(**data)

def get_all_expenses(user):
    return Expense.objects.filter(user=user)

def get_expense(user, expense_id):
    try:
        return Expense.objects.get(id=expense_id, user=user)
    except Expense.DoesNotExist:
        return None

def update_expense(user, expense_id, data):
    expense = get_expense(user, expense_id)
    if expense:
        for attr, value in data.items():
            setattr(expense, attr, value)
        expense.save()
        return expense
    return None

def delete_expense(user, expense_id):
    expense = get_expense(user, expense_id)
    if expense:
        expense.delete()
        return True
    return False
