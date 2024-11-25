from django.urls import path
from .views import UserPreferenceAPIView

urlpatterns = [
    path('<int:user_id>/preferences/', UserPreferenceAPIView.as_view(), name='user-preferences'),
]