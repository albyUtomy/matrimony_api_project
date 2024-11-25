from django.urls import path
from .views import NotificationAPIView,CreateNotificationAPIView,UpdateNotificationAPIView

urlpatterns = [
    path('create_notification/', CreateNotificationAPIView.as_view(), name='create_notification'),
    path('update_notification/<int:notification_id>/', UpdateNotificationAPIView.as_view(), name='update_notification'),
    path('<int:user_id>/notification/', NotificationAPIView.as_view(), name='get_notifications'),
]
