from django.db import transaction
from django.core.exceptions import ValidationError


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .models import UserProfile
from app_user_authentications.models import UserSetupModel
from .serializer import UserProfileSerializer
from core.validator import validate_phone_number
from .models import UserProfile
from app_connection_handler.models import FriendRequest


# Create your views here.
class CreateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_user = request.user
            user_id = current_user.user_id
            user = UserSetupModel.active_object.filter(user_id=user_id).first() 
            if not user:
                return Response({
                    'message': 'User not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            if user.profile:
                return Response({
                    'message':'Profile exists update it instead of creating'
                }, status=status.HTTP_403_FORBIDDEN)
            
            user_phone = user.phone_no if hasattr(user, 'phone_no') else None
            profile_data = request.data.copy()
            profile_data['phone_number'] = user_phone
            profile_data['user'] = user.user_id


            serializer = UserProfileSerializer(data=profile_data)
            if serializer.is_valid():
                # Save the profile with the user from the URL
                serializer.save(user=user)
                return Response({
                    'message': 'Successfully created profile.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'message': 'Invalid data.',
                'error_details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': 'An error occurred while creating the profile.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ViewProfileView(APIView):
    permission_classes = [IsAuthenticated]

    # get the profile
    def get(self, request):
        try:
            # Get the currently authenticated user
            current_user = request.user

            # Fetch the user's profile
            profile = UserProfile.objects.filter(user=current_user).first()

            if not profile:
                return Response({
                    'message': 'Profile not found.'
                }, status=status.HTTP_404_NOT_FOUND)

            # Serialize the profile data
            serializer = UserProfileSerializer(profile)

            return Response({
                'message': 'Profile retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'An error occurred while retrieving the profile.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            current_user = request.user  # The user making the request
            target_user = UserSetupModel.objects.filter(user_id=user_id).first()

            if not target_user:
                return Response({
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Check if the current user and target user have accepted each other's friend request
            friend_request = FriendRequest.objects.filter(
                sender=current_user, recipient=target_user, status=FriendRequest.ACCEPTED
            ).first() or FriendRequest.objects.filter(
                sender=target_user, recipient=current_user, status=FriendRequest.ACCEPTED
            ).first()

            # If they are not friends, remove sensitive contact details
            include_contact_details = False
            if friend_request:  # If the friend request is accepted
                include_contact_details = True

            # Get the profile of the target user
            profile = UserProfile.objects.filter(user=target_user).first()

            if not profile:
                return Response({
                    'message': 'Profile not found for this user.'
                }, status=status.HTTP_404_NOT_FOUND)

            # If contact details should not be included, remove them from the profile data
            profile_data = UserProfileSerializer(profile).data
            if not include_contact_details:
                # Remove sensitive fields from the profile data
                for field in ['username','phone_number', 'email','address']:
                    if field in profile_data:
                        del profile_data[field]

            return Response({
                'data': profile_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'An error occurred while retrieving the profile.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        try:
            current_user = request.user
            user_id = current_user.user_id
            user = UserSetupModel.active_object.filter(user_id=user_id).first() 
            if not user:
                return Response({
                    'message': 'User not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            # Fetch the user
            user = UserSetupModel.active_object.filter(user_id=user_id).first()
            if not user:
                return Response({
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Fetch the user's profile
            profile = UserProfile.objects.filter(user_id=user_id).first()
            if not profile:
                return Response({
                    'message': 'Profile not found for this user.'
                }, status=status.HTTP_404_NOT_FOUND)

            # Copy request data and begin a transaction
            profile_data = request.data.copy()
            with transaction.atomic():
                # Update phone number with validation
                if 'phone_number' in profile_data:
                    new_phone_number = profile_data['phone_number']
                    try:
                        validate_phone_number(new_phone_number)
                    except ValidationError as e:
                        return Response({
                            'message': str(e)
                        }, status=status.HTTP_400_BAD_REQUEST)

                    profile.phone_number = new_phone_number
                    user.phone_no = new_phone_number

                # Serialize and validate the profile data
                serializer = UserProfileSerializer(profile, data=profile_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    user.save()
                else:
                    return Response({
                        'message': 'Validation error occurred',
                        'errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': f'Profile updated for user {user_id}',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'An error occurred while updating the profile.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
