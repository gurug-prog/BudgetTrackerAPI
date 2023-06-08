from django.test import TestCase
from django.contrib.auth.models import User

from .models import UserProfile
from users import services

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
            first_name='Test',
            last_name='User'
        )
        cls.user_profile = UserProfile.objects.create(
            user=cls.user,
            date_of_birth='2000-01-01',
            bio='Test bio',
            profile_image=None
        )

    def test_create_user(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass',
            'first_name': 'New',
            'last_name': 'User'
        }
        user = services.create_user(data)
        self.assertIsInstance(user, User)

    def test_authenticate_user(self):
        user = services.authenticate_user('testuser@example.com', 'testpass')
        self.assertIsInstance(user, User)

    def test_get_user_profile(self):
        profile = services.get_user_profile(self.user)
        self.assertIsInstance(profile, UserProfile)

    def test_update_user_profile(self):
        data = {'bio': 'Updated bio'}
        profile = services.update_user_profile(self.user, data)
        self.assertEqual(profile.bio, 'Updated bio')
