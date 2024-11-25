# app_messaging/urls.py

from django.urls import path
from .views import SendMessageAPIView, ReceivedMessagesAPIView, UnseenMessagesAPIView

urlpatterns = [
    path('user/send_message/', SendMessageAPIView.as_view(), name='send_message'),
    path('user/received_messages/', ReceivedMessagesAPIView.as_view(), name='received_messages'),
    path('user/unseen/<int:user_id>/', UnseenMessagesAPIView.as_view(), name='unseen_messages'),
]