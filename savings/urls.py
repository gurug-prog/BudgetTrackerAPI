from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SavingViewSet

router = DefaultRouter()
router.register(r'savings', SavingViewSet, basename='saving')

urlpatterns = [
    path('', include(router.urls)),
]
