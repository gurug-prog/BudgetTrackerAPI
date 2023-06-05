from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


def create_user(data):
    return User.objects.create_user(
        username=data['email'],
        email=data['email'],
        password=data['password'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )


def authenticate_user(email, password):
    return authenticate(username=email, password=password)


def get_user_profile(user):
    return UserProfile.objects.get(user=user)


def update_user_profile(user, data):
    profile = get_user_profile(user)
    for attr, value in data.items():
        setattr(profile, attr, value)
    profile.save()
    return profile
