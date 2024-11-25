from django.urls import path
from .views import UserMatchesAPIView

urlpatterns = [
    path('matches/', UserMatchesAPIView.as_view(), name='user-matches'),
]