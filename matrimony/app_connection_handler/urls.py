from django.urls import path
from .views import SendFriendRequestAPIView, RespondToFriendRequestAPIView,ReceivedFriendRequestsAPIView

urlpatterns = [
    path('send_friend_request/<int:sender_id>/', SendFriendRequestAPIView.as_view(), name='send_friend_request'),
    path('respond_to_friend_request/<int:recipient_id>/', RespondToFriendRequestAPIView.as_view(), name='respond_to_friend_request'),
    path('received_friend_requests/<int:user_id>/', ReceivedFriendRequestsAPIView.as_view(), name='received_friend_requests'),
]
