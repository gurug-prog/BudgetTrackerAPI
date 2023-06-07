from django.urls import path, include

urlpatterns = [
    path('api/', include('users.urls')),
    path('api/', include('categories.urls')),
    path('api/', include('expenses.urls')),
    path('api/', include('savingGoals.urls')),
    path('api/', include('savings.urls')),
]
