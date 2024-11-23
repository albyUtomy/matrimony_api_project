from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from .models import Subscription
from .serializer_subscription import SubscriptionSerializer


class SubscriptionAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """Retrieve all subscriptions."""
        try:
            subscriptions = Subscription.objects.all()
            serializer = SubscriptionSerializer(subscriptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to retrieve subscriptions: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def post(self, request):
        try:
            serializer = SubscriptionSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message':'new subscription created',
                    'details':serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'message':'Invalid data input',
                'error':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message':'Failed to create',
                'error':str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request, subscription_id=None):
        try:
            subscription = Subscription.objects.get(subscription_id=subscription_id)
        except Subscription.DoesNotExist:
            return Response({
                'message':'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Failed to find subscription: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            serializer = SubscriptionSerializer(subscription, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message':f'{subscription.subscription_name} updated',
                    'data':serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'An error occurred',
                'error':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to update subscription: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request, subscription_id=None, *args, **kwargs):
        """Deactivate a subscription."""
        try:
            subscription = Subscription.objects.get(subscription_id=subscription_id)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Failed to find subscription: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            subscription.is_active = False  # Assuming an `is_active` field exists in the model
            subscription.save()
            return Response({"message": "Subscription deactivated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to deactivate subscription: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)