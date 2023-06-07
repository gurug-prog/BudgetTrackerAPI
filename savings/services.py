from .models import Saving


def create_saving(user, data):
    data['user'] = user
    return Saving.objects.create(**data)


def get_all_savings(user):
    return Saving.objects.filter(user=user)


def get_saving(user, saving_id):
    try:
        return Saving.objects.get(id=saving_id, user=user)
    except Saving.DoesNotExist:
        return None


def update_saving(user, saving_id, data):
    saving = get_saving(user, saving_id)
    if saving:
        for attr, value in data.items():
            setattr(saving, attr, value)
        saving.save()
        return saving
    return None


def delete_saving(user, saving_id):
    saving = get_saving(user, saving_id)
    if saving:
        saving.delete()
        return True
    return False
