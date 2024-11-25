
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from app_user_authentications.models import UserSetupModel
from .models import Message
from .serializers import MessageSerializer





class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the sender user based on the passed sender_id
        try:
            sender_id = request.user.user_id
            sender = UserSetupModel.objects.get(user_id=sender_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "Sender user not found"}, status=status.HTTP_404_NOT_FOUND)

        recipient_id = request.data.get('recipient')
        content = request.data.get('content')
        image = request.FILES.get('image')  # This gets the image file from the request

        # Check if the recipient exists
        try:
            recipient = UserSetupModel.objects.get(user_id=recipient_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "Recipient user not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the recipient has blocked the sender
        if recipient.blocked_users.filter(user_id=sender.user_id).exists():
            return Response({"error": "You have been blocked by the recipient and cannot send a message."}, status=status.HTTP_403_FORBIDDEN)

        # Create a new message with optional text and image
        try:
            message = Message.objects.create(
                sender=sender,
                recipient=recipient,
                content=content,
                image=image,  # Image is optional
                status='unseen'  # Initially, mark the message as unseen
            )
        except Exception as e:
            return Response({"error": f"Failed to send message: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the response
        serializer = MessageSerializer(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ReceivedMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the recipient user based on the passed user_id
        try:
            user_id = request.user.user_id
            recipient = UserSetupModel.objects.get(user_id=user_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "Recipient user not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all messages where the current user is the recipient
        received_messages = Message.objects.filter(recipient=recipient)

        # Mark messages as read (seen) and update the status
        for message in received_messages:
            if message.status == 'unseen':
                message.mark_as_read()

        # Serialize and return the messages
        serializer = MessageSerializer(received_messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UnseenMessagesAPIView(APIView):

    def get(self, request, user_id=None, *args, **kwargs):
        # Get the recipient user based on the passed user_id
        try:
            recipient = UserSetupModel.objects.get(user_id=user_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "Recipient user not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all unseen messages where the current user is the recipient
        unseen_messages = Message.objects.filter(recipient=recipient, status='unseen')

        # Serialize and return the unseen messages
        serializer = MessageSerializer(unseen_messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)