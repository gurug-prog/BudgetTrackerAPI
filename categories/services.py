from .models import Category


def create_category(data):
    return Category.objects.create(**data)


def get_all_categories():
    return Category.objects.all()


def get_category(category_id):
    try:
        return Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return None


def update_category(category_id, data):
    category = get_category(category_id)
    if category:
        for attr, value in data.items():
            setattr(category, attr, value)
        category.save()
        return category
    return None


def delete_category(category_id):
    category = get_category(category_id)
    if category:
        category.delete()
        return True
    return False
