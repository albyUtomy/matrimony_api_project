from django.urls import path
from .views import CreateProfileView, UpdateUserProfileView

urlpatterns = [
    path('<int:user_id>/add_profile/', CreateProfileView.as_view(), name='create-profile'),
    path('<int:user_id>/update_profile/', UpdateUserProfileView.as_view(), name='update-profile'),

]
