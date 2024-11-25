from rest_framework import serializers
from .models import UserPreference
from app_admin.models import CategoryValue

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = [
            'user','religion', 'caste', 'profession', 'education', 'language','gender',
            'age_min', 'age_max', 'height_min', 'height_max','marital_status'
        ]  # Include all relevant fields
    
    def validate(self, data):
        """
        Validate category-based fields against the CategoryValue table.
        """
        # Validate category-based fields
        category_fields = {
            'gender': data.get('gender'),
            'religion':data.get('religion'),
            'caste': data.get('caste'),
            'profession': data.get('profession'),
            'education': data.get('education'),
            'language': data.get('language'),
            'marital_status':data.get('marital_status'),
            'location':data.get('location')
        }

        for field, value in category_fields.items():
            if value and not CategoryValue.objects.filter(
                category_id__category_name__iexact=field,
                category_value__iexact=value
            ).exists():
                # Fetch all valid values for the category
                valid_values = CategoryValue.objects.filter(
                    category_id__category_name__iexact=field
                ).values_list('category_value', flat=True)
                
                raise serializers.ValidationError({
                    field: f"'{value}' is not a valid {field} option.",
                    "valid_fields": list(valid_values)  # Include valid options in the error
                })

        # Validate age range
        age_min = data.get('age_min')
        age_max = data.get('age_max')
        if age_min and age_max and age_min > age_max:
            raise serializers.ValidationError({
                'age_min': "Minimum age cannot be greater than maximum age.",
                'age_max': "Maximum age cannot be less than minimum age."
            })

        # Validate height range
        height_min = data.get('height_min')
        height_max = data.get('height_max')
        if height_min and height_max and height_min > height_max:
            raise serializers.ValidationError({
                'height_min': "Minimum height cannot be greater than maximum height.",
                'height_max': "Maximum height cannot be less than minimum height."
            })

        return data
