from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import UserProfile
from app_user_authentications.models import UserSetupModel
from .serializer import UserProfileSerializer
from core.validator import validate_phone_number
from django.core.exceptions import ValidationError

# Create your views here.

class CreateProfileView(APIView):
    def post(self, request, user_id):
        try:
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
        

class UpdateUserProfileView(APIView):
    def put(self, request, user_id):
        try:
            user = UserSetupModel.active_object.filter(user_id=user_id).first()
            if not user:
                return Response({
                    'message':'User not found'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            profile = UserProfile.objects.filter(user_id=user_id).first()

            if not profile:
                return Response({
                    'message': 'Profile not found for this user.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            profile_data = request.data.copy()
            profile.user = user #Ensure the user_id remain same

            if 'phone_number' in profile_data:
                new_phone_number = request.data['phone_number']
                try:
                    validate_phone_number(new_phone_number)
                except ValidationError as e:
                    return Response({
                        'message':str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)
                profile.phone_number = new_phone_number
                user.phone_no = new_phone_number
            profile.save()

            serializer = UserProfileSerializer(profile, partial=True)
            return Response({
                'message':f'Profile updated for the user{profile.user.user_id}',
                'data':serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'message': 'An error occurred while updating the profile.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)