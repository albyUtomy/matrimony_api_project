from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer
from app_user_authentications.models import UserSetupModel



class NotificationAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        # Fetch notifications for the specific user
        try:
            user = UserSetupModel.objects.get(id=user_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        
        # Serialize the notifications
        serializer = NotificationSerializer(notifications, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateNotificationAPIView(APIView):
    # Ensure only admin users can create notifications
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        # Get data from the request
        user_id = request.data.get('user_id')
        notification_type = request.data.get('notification_type')
        message = request.data.get('message')
        
        # Validate the input data
        if not user_id or not notification_type or not message:
            return Response({"error": "Missing required fields (user_id, notification_type, message)"}, 
                             status=status.HTTP_400_BAD_REQUEST)
        
        # Get the user to send the notification to
        try:
            user = UserSetupModel.objects.get(id=user_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.is_admin:
            return Response({
                'message':'Unauthorized access try found, only admin can create notification'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Create the notification
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            message=message,
            is_seen=False  # Default to unseen
        )
        
        # Serialize and return the notification data
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateNotificationAPIView(APIView):
    # Ensure only admin users can update notifications
    permission_classes = [permissions.IsAdminUser]
    
    def put(self, request, notification_id=None, *args, **kwargs):
        # Get the notification to be updated
        try:
            notification = Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the request user is an admin
        if not request.user.is_staff:
            return Response({
                'message': 'Unauthorized access, only admin can update notifications'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Get the data from the request
        notification_type = request.data.get('notification_type')
        message = request.data.get('message')
        is_seen = request.data.get('is_seen')

        # Update fields if provided
        if notification_type:
            notification.notification_type = notification_type
        if message:
            notification.message = message
        if is_seen is not None:
            notification.is_seen = is_seen

        # Save the changes
        notification.save()

        # Serialize and return the updated notification data
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class MarkNotificationsAsSeenAPIView(APIView):
    def post(self, request, user_id, *args, **kwargs):
        # Mark notifications as seen
        notifications = Notification.objects.filter(user_id=user_id, is_seen=False)
        notifications.update(is_seen=True)
        
        return Response({"message": "Notifications marked as seen"}, status=status.HTTP_200_OK)
