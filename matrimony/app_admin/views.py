from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# local import
from .models import Category, CategoryValue
from .serializer import CategorySerializer, CategoryValuesSerializer,CategoryValueListSerializer


# Create your views here.
class CreateCategoryView(APIView):
    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message':'New category created',
                    'data':serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'error_message':'Invalid data',
                'error':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': 'Internal Error',
                'error':str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AddCategoryValuesView(APIView):
    def post(self, request, category_id):
        try:
            # Get the category from the ID
            category = Category.objects.get(category_id=category_id)
            
            # Get the list of category values from the request
            category_values = request.data.get('category_values', [])
            
            if not category_values:
                return Response({
                    'message': 'No category values provided.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate each value and add it to the category if it doesn't already exist
            for value in category_values:
                # Check if the value already exists for the category
                if CategoryValue.objects.filter(category_id=category, category_value__iexact=value).exists():
                    return Response({
                        'message': f"The value '{value}' already exists in the category {category.category_name}."
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Create the new category value
                CategoryValue.objects.create(category_id=category, category_value=value)

            return Response({
                'message': f"{len(category_values)} values successfully added to the category {category.category_name}."
            }, status=status.HTTP_201_CREATED)

        except Category.DoesNotExist:
            return Response({
                'message': 'Category not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': 'An error occurred.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateCategory(APIView):
    def put(self, request, category_id):
        try:
            category = Category.objects.get(category_id=category_id)
        except Category.DoesNotExist:
            return Response({
                'message': f"Category with ID {category_id} not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            new_category_name = serializer.validated_data.get('category_name', category.category_name).capitalize()

            if Category.objects.filter(category_name__iexact=new_category_name).exclude(category_id=category_id).exists():
                return Response({
                    'message':f"A category with the name '{new_category_name}' already exists."
                    }, status=status.HTTP_403_FORBIDDEN)
            category.category_name = new_category_name
            category.save()
            
            return Response({
                'message': f"Category '{new_category_name}' updated successfully."
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error_message': 'Invalid data',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateCategoryValues(APIView):
    def put(self, request,category_id, category_value_id):
        try:
            # Retrieve the Category object using category_id
            category = Category.objects.get(category_id=category_id)
        except Category.DoesNotExist:
            return Response({
                'message': f"Category with ID {category_id} not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            category_value = CategoryValue.objects.get(id=category_value_id, category_id=category)
        except CategoryValue.DoesNotExist:
            return Response({
                'message': f"Category value with ID {category_value_id} not found in this category."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategoryValuesSerializer(category_value, data=request.data, partial=True)
        
        if serializer.is_valid():
            new_category_value = serializer.validated_data.get('category_value', category_value.category_value).capitalize()
            
            if CategoryValue.objects.filter(category_id=category, category_value__iexact=new_category_value).exclude(id=category_value_id).exists():
                return Response({
                    'message': f"A category value with the name '{new_category_value}' already exists in this category."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Save the updated category value
            category_value.category_value = new_category_value
            category_value.save()
            
            return Response({
                'message': f"Category value '{new_category_value}' updated successfully."
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error_message': 'Invalid data',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class ListCategory(APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({
                'message':serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "An error occurred while fetching categories.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ListCategoryValues(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(category_id=category_id)
            category_values = CategoryValue.objects.filter(category_id=category_id).values_list('category_value', flat=True)

            if not category_values.exists():
                return Response({
                    'message': f"No values found for the category with ID {category_id}."
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'category_id': category_id,
                'category_name': category.category_name,
                'category_values': list(category_values)
            }, status=status.HTTP_200_OK)
        
        except Category.DoesNotExist:
            return Response({
                'message': f"Category with ID {category_id} not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred while fetching category values.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteCategoryAndValues(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, category_id):
        try:
            if not request.user.is_admin:
                return Response({
                    'message':'Normal user cannot use admin privileges'
                }, status=status.HTTP_401_UNAUTHORIZED)
            # Check if category exists
            category = Category.objects.get(category_id=category_id)

            # Delete all CategoryValue instances related to this category
            CategoryValue.objects.filter(category_id=category_id).delete()

            # Delete the category
            category.delete()

            return Response({
                'message': f"Category with ID {category_id} and all its values have been deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        
        except Category.DoesNotExist:
            return Response({
                'message': f"Category with ID {category_id} not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'message': "An error occurred while deleting the category.",
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
