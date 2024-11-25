from django.urls import path
from .views import CreateProfileView, UpdateUserProfileView,ViewProfileView,GetUserProfileView

urlpatterns = [
    path('add_profile/', CreateProfileView.as_view(), name='create-profile'),
    path('view_profile/', ViewProfileView.as_view(), name='view-profile'),
     path('search_profile/<int:user_id>/', GetUserProfileView.as_view(), name='get_user_profile'),
    path('update_profile/', UpdateUserProfileView.as_view(), name='update-profile'),

]
