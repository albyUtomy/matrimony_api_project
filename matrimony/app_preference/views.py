from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import UserPreference
from .serializers import UserPreferenceSerializer
from app_user_authentications.models import UserSetupModel  # Replace with the actual User model


class UserPreferenceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_preferences(self, user_id):
        return UserPreference.objects.filter(user_id=user_id).first()

    def get(self, request):
        try:
            user_preferences = UserPreference.objects.filter(user_id=request.user.user_id).first()
            if not user_preferences:
                return Response({"error": "User preferences not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserPreferenceSerializer(user_preferences)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        try:
            current_user = request.user
            user_id = current_user.user_id
            user = UserSetupModel.active_object.filter(user_id=user_id).first()

            if not user:
                return Response({
                    'message': 'User not found.'
                }, status=status.HTTP_404_NOT_FOUND)

            # Check if the user already has preferences
            if user.preference:
                return Response({
                    'message': 'Preferences already exist. Update them instead of creating new ones.'
                }, status=status.HTTP_403_FORBIDDEN)

            preference_data = request.data.copy()
            preference_data['user'] = user.user_id

            serializer = UserPreferenceSerializer(data=preference_data)
            if serializer.is_valid():
                # Save the preferences with the user
                user_preference = serializer.save()
                user.preference = user_preference  # Assign the UserPreference instance
                user.save()

                return Response({
                    'message': 'Preferences successfully created.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                'message': 'Invalid data.',
                'error_details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': 'An error occurred while creating preferences.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    
                                
    def put(self, request):
        try:
            user_preferences = UserPreference.objects.filter(user_id=request.user.user_id).first()
            if not user_preferences:
                return Response({"error": "User preferences not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserPreferenceSerializer(user_preferences, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Successfully updated.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({"message": "Invalid data.", "error_details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred while updating preferences.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
