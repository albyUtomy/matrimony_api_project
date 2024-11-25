from django.urls import path
from .views import UserPreferenceAPIView

urlpatterns = [
    path('preferences/', UserPreferenceAPIView.as_view(), name='user-preferences'),
]