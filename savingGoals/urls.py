from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SavingGoalViewSet

router = DefaultRouter()
router.register(r'saving-goals', SavingGoalViewSet, basename='saving_goal')

urlpatterns = [
    path('', include(router.urls)),
]
