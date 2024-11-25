from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FriendRequest, BlockedUser
from app_user_authentications.models import UserSetupModel
from .serializers import FriendRequestSerializer


class SendFriendRequestAPIView(APIView):
    def post(self, request, sender_id=None, *args, **kwargs):
        sender = UserSetupModel.objects.get(user_id=sender_id)
        recipient_id = request.data.get('recipient')

        try:
            recipient = UserSetupModel.objects.get(user_id=recipient_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "Recipient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the sender and recipient are the same
        if sender == recipient:
            return Response({"error": "You cannot send a friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a request already exists
        if FriendRequest.objects.filter(sender=sender, recipient=recipient).exists():
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the friend request
        FriendRequest.objects.create(sender=sender, recipient=recipient, status=FriendRequest.PENDING)

        return Response({"message": "Friend request sent successfully"}, status=status.HTTP_201_CREATED)



# class RespondToFriendRequestAPIView(APIView):
#     def post(self, request, recipient_id=None, *args, **kwargs):
#         # Get the recipient user based on the passed recipient_id
#         try:
#             recipient = UserSetupModel.objects.get(user_id=recipient_id)
#         except UserSetupModel.DoesNotExist:
#             return Response({"error": "Recipient not found"}, status=status.HTTP_404_NOT_FOUND)

#         sender_id = request.data.get('sender')
#         status_update = request.data.get('status')  # 'accepted', 'rejected', 'blocked'

#         # Check if sender exists
#         try:
#             sender = UserSetupModel.objects.get(user_id=sender_id)
#         except UserSetupModel.DoesNotExist:
#             return Response({"error": "Sender not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the friend request exists
#         try:
#             friend_request = FriendRequest.objects.get(sender=sender, recipient=recipient)
#         except FriendRequest.DoesNotExist:
#             return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Handle the response based on the status
#         if status_update == 'accepted':
#             friend_request.status = FriendRequest.ACCEPTED
#             friend_request.save()
#             return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
        
#         elif status_update == 'rejected':
#             friend_request.status = FriendRequest.REJECTED
#             friend_request.save()
#             return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)

#         elif status_update == 'blocked':
#             # Check if the user has already blocked the sender
#             if BlockedUser.objects.filter(blocker=recipient, blocked=sender).exists():
#                 return Response({"error": "You have already blocked this user"}, status=status.HTTP_400_BAD_REQUEST)

#             # Block the sender and add the sender to blocked_users
#             BlockedUser.objects.create(blocker=recipient, blocked=sender)
#             # Update the friend request to blocked
#             friend_request.status = FriendRequest.BLOCKED
#             friend_request.save()
            
#             # Prevent the blocked user from sending further messages or interactions
#             recipient.blocked_users.add(sender)

#             return Response({"message": "User blocked and friend request marked as blocked"}, status=status.HTTP_200_OK)

#         return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)



class ReceivedFriendRequestsAPIView(APIView):
    
    def get(self, request, user_id=None, *args, **kwargs):
        # Get the recipient user based on the passed user_id
        try:
            recipient = UserSetupModel.objects.get(user_id=user_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "Recipient user not found"}, status=status.HTTP_404_NOT_FOUND)
    
        # Get all friend requests where the current user is the recipient
        received_requests = FriendRequest.objects.filter(recipient=recipient)

        # Serialize the friend requests
        serializer = FriendRequestSerializer(received_requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RespondToFriendRequestAPIView(APIView):
    def post(self, request, recipient_id=None, *args, **kwargs):
        # Get the recipient user based on the passed recipient_id
        try:
            recipient = UserSetupModel.objects.get(user_id=recipient_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "Recipient not found"}, status=status.HTTP_404_NOT_FOUND)

        sender_id = request.data.get('sender')
        status_update = request.data.get('status')  # 'accepted', 'rejected', 'blocked', 'unblocked'

        # Check if sender exists
        try:
            sender = UserSetupModel.objects.get(user_id=sender_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "Sender not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the friend request exists
        try:
            friend_request = FriendRequest.objects.get(sender=sender, recipient=recipient)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        # Handle the response based on the status
        if status_update == 'accepted':
            friend_request.status = FriendRequest.ACCEPTED
            friend_request.save()
            return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
        
        elif status_update == 'rejected':
            friend_request.status = FriendRequest.REJECTED
            friend_request.save()
            return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)

        elif status_update == 'blocked':
            # Check if the user has already blocked the sender
            if BlockedUser.objects.filter(blocker=recipient, blocked=sender).exists():
                return Response({"error": "You have already blocked this user"}, status=status.HTTP_400_BAD_REQUEST)

            # Block the sender and add the sender to blocked_users
            BlockedUser.objects.create(blocker=recipient, blocked=sender)
            # Update the friend request to blocked
            friend_request.status = FriendRequest.BLOCKED
            friend_request.save()
            
            # Prevent the blocked user from sending further messages or interactions
            recipient.blocked_users.add(sender)

            return Response({"message": "User blocked and friend request marked as blocked"}, status=status.HTTP_200_OK)

        elif status_update == 'unblocked':
            # Check if the user has blocked the sender
            try:
                blocked_user = BlockedUser.objects.get(blocker=recipient, blocked=sender)
                blocked_user.delete()  # Unblock the user
                recipient.blocked_users.remove(sender)  # Remove from blocked_users
                # Update the friend request to unblocked
                friend_request.status = FriendRequest.PENDING  # Set status back to pending if needed
                friend_request.save()
                
                return Response({"message": "User unblocked and friend request status updated to pending"}, status=status.HTTP_200_OK)
            except BlockedUser.DoesNotExist:
                return Response({"error": "You have not blocked this user"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
