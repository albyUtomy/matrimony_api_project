from django.urls import path
from .views import (
    CreateUser,
    UserListView, 
    UserRetrieveUpdateView, 
    UserDeactivate, 
    ListOnlyAdmin, 
    ListInActiveUser, 
    UserLoginView, 
    UserLogOutView, 
    UserReactivate,
    ListBlockedUsers
    )

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="user-login"),
    path('logout/', UserLogOutView.as_view(), name="user-logout"),
    path('create_user/', CreateUser.as_view(), name='user-create'),
    path('list_users/', UserListView.as_view(), name='user-create'),
    path('admin/', ListOnlyAdmin.as_view(), name='user-list-create'),
    path('user/<int:user_id>/', UserRetrieveUpdateView.as_view(), name='user-retrieve-update'),
    path('user/deactivate/', UserDeactivate.as_view(), name='user-deactivate'),
    path('user/reactivate/<int:user_id>/', UserReactivate.as_view(), name='user-deactivate'),
    path('inactive', ListInActiveUser.as_view(), name='inactive-user-list'),
    path('blocked-users/', ListBlockedUsers.as_view(), name='list-blocked-users'),
]