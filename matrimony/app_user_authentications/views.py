# imports from django
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now

# imports from rest_framework
from rest_framework.generics  import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, APIException

# other imports
from .serializers import UserSerializer, InactiveUserSerializer, UserLoginSerializer,UserUpdateSerializer
from .models import UserSetupModel
from .permissions import OnlyAdmin
from app_connection_handler.serializers import BlockedUserSerializer
from app_connection_handler.models import BlockedUser
from app_user_history.models import TokenStorage
from .utils import deactivate_user

import logging

# Set up a logger for better debugging
logger = logging.getLogger(__name__)


# Create your views here.
class CreateUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            if request.user and request.user.is_authenticated:
                return Response({
                    'message':'Authenticated users cannot create another account.',
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['is_admin'] = False
                serializer.save()
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


class CreateAdminUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            if not request.user.is_admin:
                return Response({
                    'message':'Unauthorized access',
                })
            
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                serializer.validated_data['is_admin'] = True
                serializer.save()
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
    permission_classes = [OnlyAdmin]
    def get(self, request):
        try:
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

    permission_classes = [AllowAny]
    def post(self, request):
        try:
            if request.user and request.user.is_authenticated:
                return Response({
                    'message':'Authenticated users cannot login to another account.',
                },status=status.HTTP_400_BAD_REQUEST)
            
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
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            print(f"Generated tokens for user {username}")

            # Saving token in TokenStorage Model
            TokenStorage.objects.create(
                user=user,
                access_token=access_token,
                refresh_token=refresh_token
                )

            return Response({
                'access': access_token,
                'refresh': str(refresh_token),
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Log exception for better debugging
            print(f"Error during login: {str(e)}")
            return Response({
                "message": "An error occurred during login",
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_id = request.user.user_id
            user = UserSetupModel.active_object.get(user_id=user_id)
            serializer = UserSerializer(user)
            return Response({
                'message':'Current user details',
                'user data':serializer.data
            },status=status.HTTP_200_OK)
        
        except UserSetupModel.DoesNotExist:
            return Response({
                'message':'User not logged in'
            })
        except Exception as e:
            return Response({
                'message':'Internal Issues',
                'error_message':str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    permission_classes = [OnlyAdmin]
    serializer_class = UserSerializer
    def get_queryset(self):
        try:
            queryset = UserSetupModel.active_object.all()
            return queryset
        except UserSetupModel.DoesNotExist():
            raise NotAuthenticated({
                'message':'Admin login required'
                },status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            raise APIException({
                'message':'an error occurred',
                'error_details':str(e)
            },status=status.HTTP_400_BAD_REQUEST)

    
class UpdateCurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            
            if serializer.is_valid():
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
    def delete(self, request, user_id=None):
        try:
            current_user = request.user
            if user_id is None:
                user_id = current_user.user_id

            try:
                user_to_deactivate = UserSetupModel.objects.get(user_id=current_user.user_id)
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
            
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({
                    'error_message':'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if user_to_deactivate:
                deactivate_user(user_to_deactivate, current_user.user_id, refresh_token)
            return Response({
                "message": f"User {user_to_deactivate.username} deleted successfully"
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class UserReactivate(APIView):
    permission_classes = [OnlyAdmin]
    def put(self, request):
        try:
            user_id = request.data['user_id']
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

            deactivate_user(user_to_reactivate, user_id)

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
    permission_classes = [OnlyAdmin]
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
