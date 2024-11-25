# imports from django
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now

# imports from rest_framework
from rest_framework.generics  import ListCreateAPIView,RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
"""from rest_framework.authtoken.models import Token"""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

# other imports
from .serializers import UserSerializer, InactiveUserSerializer, UserLoginSerializer
from .models import UserSetupModel
from app_connection_handler.serializers import BlockedUserSerializer
from app_connection_handler.models import BlockedUser

import logging

# Set up a logger for better debugging
logger = logging.getLogger(__name__)


# Create your views here.
class CreateUser(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data, many=True)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'message':'User created successfully',
                    'user':serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message':'Invalid data',
                    'error':serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'message':'An error occurred while creating the user',
                'error':str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            current_user = request.user
            if not current_user.is_admin:
                return Response({
                "message": "Unauthorized access user is not an admin"
            }, status=status.HTTP_403_FORBIDDEN)

            users = UserSetupModel.active_object.all()
            serializer = UserSerializer(users, many=True)
            return Response({
                'message': 'User list retrieved successfully',
                'users': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Return error response in case of any unexpected errors
            return Response({
                'message': 'An error occurred while retrieving the user list',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class UserLoginView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)

            # Validate the data
            if not serializer.is_valid():
                return Response({
                    'message': 'Invalid data',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            if not username or not password:
                return Response({
                    'message': 'Username and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Authenticate the user
            print("username and password:", username, password)
            user = authenticate(request, username=username, password=password)
            print(f"Attempting login for user: {username}")

            if user is None:
                # Log the failure for debugging
                return Response({
                    'message': 'User not found or password mismatch'
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Check if the user already has an active token
            active_tokens = OutstandingToken.objects.filter(user=user)
            for token in active_tokens:
                if not BlacklistedToken.objects.filter(token=token).exists():
                    return Response({
                        'message': f"User '{user.username}' is already logged in."
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Log the user in
            login(request, user)
            print(f"Authenticated user with ID: {user.user_id}")

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            print(f"Generated tokens for user {username}")

            return Response({
                'access': access_token,
                'refresh': str(refresh),
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Log exception for better debugging
            print(f"Error during login: {str(e)}")
            return Response({
                "message": "An error occurred during login",
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserLogOutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({
                    'error_message':'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out, refresh token invalidated"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListOnlyAdmin(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        # Filter users by the 'is_admin' status if needed
        queryset = UserSetupModel.active_object.all()

        is_admin = self.request.query_params.get('is_admin', True)
        if is_admin is not None:
            queryset = queryset.filter(is_admin=is_admin)
        return queryset
    
class UpdateCurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def put(self, request, *args, **kwargs):
        try:
            # Get the currently authenticated user
            user = request.user

            # Use the serializer to validate and update user data
            serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True allows updating only provided fields
            
            if serializer.is_valid():
                # Save the updated user details
                serializer.save()

                return Response({
                    'message': 'User updated successfully.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'message': 'Invalid data.',
                'error_details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': 'An error occurred while updating user.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDeactivate(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, user_id=None):
        try:
            current_user = request.user

            if user_id is None:
                user_id = current_user.user_id

            try:
                user_to_deactivate = UserSetupModel.objects.get(user_id=user_id)
            except UserSetupModel.DoesNotExist:
                return Response({
                    'message':'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            if not (current_user.is_admin or current_user.user_id == user_to_deactivate.user_id):
                return Response({
                    "message": "Unauthorized: Only admins or the user themselves can deactivate."
                }, status=status.HTTP_403_FORBIDDEN)
            
            if not user_to_deactivate.is_active:
                return Response({
                    'message':'User already deleted'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user_to_deactivate.is_active = False
            user_to_deactivate.save()

            if user_to_deactivate.profile:
                user_to_deactivate.profile.is_active = False
                user_to_deactivate.profile.save()

            return Response({
                "message": f"User {user_to_deactivate.username} deleted successfully"
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class UserReactivate(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, user_id=None):
        try:
            current_user = request.user
            if not current_user.is_admin:
                return Response({
                    'message':'Unauthorized : Only admin can reactivate users'
                }, status=status.HTTP_403_FORBIDDEN)
            
            if not user_id:
                return Response({
                    'message':'User id is required to reactivate a user'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # attempt to find the user id
            try:
                user_to_reactivate = UserSetupModel.objects.get(user_id=user_id)
            except UserSetupModel.DoesNotExist:
                return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # reactivate the user
            if user_to_reactivate.is_active:
                return Response({
                    "message": f"User {user_to_reactivate.username} is already active."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if user_to_reactivate.is_active:
                return Response({
                    'message':'User already active'
                }, status=status.HTTP_400_BAD_REQUEST)

            user_to_reactivate.is_active = True
            user_to_reactivate.save()

            return Response({
                "message": f"User {user_to_reactivate.username} reactivated successfully."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle unexpected exceptions
            print("Error during reactivation:", e)
            return Response({
                "message": "An error occurred while reactivating the user.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
# LIst inactive user
class ListInActiveUser(ListAPIView):
    serializer_class = InactiveUserSerializer
    def get_queryset(self):
        query_set = UserSetupModel.inactive_object.all()
        return query_set
    
class ListBlockedUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({
                'message': 'Unauthorized access, only admin can access'
            }, status=status.HTTP_401_UNAUTHORIZED)
        

        blocked_users = BlockedUser.objects.all()
        
        # Check if the list is empty
        if not blocked_users.exists():
            return Response({
                'message': 'The list of blocked users is empty.'
            }, status=status.HTTP_200_OK)
        
        # Serialize and return the blocked users
        serializer = BlockedUserSerializer(blocked_users, many=True)
        return Response({
            'message': 'List of blocked users with blockers.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
