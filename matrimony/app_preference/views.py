from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import UserPreference
from .serializers import UserPreferenceSerializer
from app_user_authentications.models import UserSetupModel  # Replace with the actual User model

class UserPreferenceAPIView(APIView):
    """
    API View for creating, updating, and retrieving user preferences.
    """

    def get(self, request, user_id, *args, **kwargs):
        """Retrieve user preferences by user ID."""
        try:
            user_preferences = UserPreference.objects.get(user_id=user_id)
            serializer = UserPreferenceSerializer(user_preferences)
            return Response({
                'data':serializer.data}, status=status.HTTP_200_OK)
        except UserPreference.DoesNotExist:
            return Response({"error": "User preferences not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, user_id, *args, **kwargs):
        """Create user preferences for a user by user ID."""
        try:
            try:
                user = UserSetupModel.objects.get(user_id=user_id)
            except UserSetupModel.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            data = request.data.copy()
            data['user'] = user.user_id

            serializer = UserPreferenceSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message':'successfully added',
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
        

    def put(self, request, user_id, *args, **kwargs):
        """Update user preferences for a user by user ID."""
        try:
            try:
                user_preferences = UserPreference.objects.get(user_id=user_id)
            except UserPreference.DoesNotExist:
                return Response({"error": "User preferences not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserPreferenceSerializer(user_preferences, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message':'updated successfully',
                    'data': serializer.data
                    }, status=status.HTTP_200_OK)
            
            return Response({
                    'message': 'Invalid data.',
                    'error_details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': 'An error occurred while creating the profile.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
