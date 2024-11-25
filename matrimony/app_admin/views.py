from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# local import
from .models import Category, CategoryValue
from .serializer import CategorySerializer, CategoryValuesSerializer,CategoryValueListSerializer
from core.permissions import IsAdminUser
# Create your views here.
class CreateCategoryView(APIView):
    # permission_classes = [IsAdminUser]

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
    # permission_classes = [IsAdminUser]

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

            # Serialize the data with the CategoryValuesSerializer
            serializer = CategoryValuesSerializer(data={
                'category_id': category_id,
                'category_values': category_values
            })

            if serializer.is_valid():
                # Create new category values using the validated (capitalized) data
                category_values_to_create = [
                    CategoryValue(category_id=category, category_value=value)
                    for value in serializer.validated_data['category_values']
                ]
                CategoryValue.objects.bulk_create(category_values_to_create)

                return Response({
                    'message': f"{len(category_values)} values successfully added to the category '{category.category_name}'.",
                    'updated_values': serializer.validated_data['category_values']
                }, status=status.HTTP_201_CREATED)

            return Response({
                'message': 'Invalid data',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

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
    # permission_classes = [IsAdminUser]

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
    # permission_classes = [IsAdminUser]

    def put(self, request, category_id, category_value_id):
        try:
            # Validate the existence of the Category
            category = Category.objects.get(category_id=category_id)
        except Category.DoesNotExist:
            return Response({
                'message': f"Category with ID {category_id} not found."
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            # Validate the existence of the specific CategoryValue
            category_value = CategoryValue.objects.get(value_id=category_value_id, category_id=category)
        except CategoryValue.DoesNotExist:
            return Response({
                'message': f"Category value with ID {category_value_id} not found for category ID {category_id}."
            }, status=status.HTTP_404_NOT_FOUND)

        # Deserialize and validate the input data
        serializer = CategoryValuesSerializer(category_value, data=request.data, partial=True)

        if serializer.is_valid():
            # Process the new values
            new_category_values = serializer.validated_data.get('category_values', [])

            # Capitalize each value for consistent storage
            capitalized_values = [value.capitalize() for value in new_category_values]

            # Ensure all new values are unique within this category
            for value in capitalized_values:
                if CategoryValue.objects.filter(
                    category_id=category,
                    category_value__iexact=value
                ).exclude(value_id=category_value_id).exists():
                    return Response({
                        'message': f"A category value '{value}' already exists in this category."
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Update and save the category values
            category_value.category_value = ", ".join(capitalized_values)  # Adjust as per your field structure
            category_value.save()

            return Response({
                'message': f"Category value(s) updated successfully for category ID {category_id}.",
                'updated_values': capitalized_values
            }, status=status.HTTP_200_OK)

        # Handle validation errors
        return Response({
            'error_message': 'Invalid data',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class ListCategory(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            # Fetch all categories
            categories = Category.objects.all()
            category_data = []

            for category in categories:
                # Fetch the values for each category
                category_values = CategoryValue.objects.filter(category_id=category).values_list('category_value', flat=True)
                
                category_data.append({
                    'category_id':category.category_id,
                    'category_name': category.category_name,
                    'category_values': list(category_values)
                })

            return Response(category_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "An error occurred while fetching categories.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ListCategoryValues(APIView):
    # permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]
    def delete(self, request, category_id):
        try:
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
