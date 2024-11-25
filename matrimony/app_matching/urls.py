from django.urls import path
from .views import UserMatchesAPIView

urlpatterns = [
    path('<int:user_id>/matches/', UserMatchesAPIView.as_view(), name='user-matches'),
]