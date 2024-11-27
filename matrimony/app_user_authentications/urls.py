from django.urls import path
from .views import (
    CreateUser,
    UserListView, 
    UpdateCurrentUserAPIView, 
    UserDeactivate, 
    ListOnlyAdmin, 
    ListInActiveUser, 
    UserLoginView, 
    UserLogOutView, 
    UserReactivate,
    ListBlockedUsers,
    CreateAdminUser,
    UserDetails
    )

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="user-login"),
    path('logout/', UserLogOutView.as_view(), name="user-logout"),
    path('create_user/', CreateUser.as_view(), name='user-create'),
    path('create_admin_user/', CreateAdminUser.as_view(), name='create-admin'),
    path('user-details/',UserDetails.as_view(), name='user-details'),
    path('list_users/', UserListView.as_view(), name='user-create'),
    path('admin/', ListOnlyAdmin.as_view(), name='user-list-create'),
    path('user/update/', UpdateCurrentUserAPIView.as_view(), name='user-retrieve-update'),
    path('user/deactivate/', UserDeactivate.as_view(), name='user-deactivate'),
    path('user/reactivate/<int:user_id>/', UserReactivate.as_view(), name='user-deactivate'),
    path('inactive', ListInActiveUser.as_view(), name='inactive-user-list'),
    path('blocked-users/', ListBlockedUsers.as_view(), name='list-blocked-users'),
]