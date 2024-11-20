from rest_framework import serializers
from .models import UserProfileModel
from app_admin.models import CategoryValue
from .validator import validate_category_fields

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = [
            'user_id', 'age', 'gender', 'dob', 'bio', 'weight', 'height',
            'religion', 'caste', 'income', 'profession', 'education',
            'address', 'language'
        ]


    def validate(self, data):
        """
        Validate category-based fields using the validate_category_field function.
        """
        category_fields = ['gender', 'religion', 'caste', 'profession', 'education']
        
        for field in category_fields:
            value = data.get(field)
            if value:  # Only validate if the field is provided
                validate_category_fields(field, value)
        return data