from rest_framework import serializers
from .models import UserProfile
from app_admin.models import CategoryValue

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user', 'age', 'gender', 'dob', 'bio', 'weight', 'height',
            'religion', 'caste', 'income', 'profession', 'education',
            'address', 'language'
        ]

    def validate(self, data):
        """
        Validate category-based fields against the CategoryValue table.
        """
        category_fields = {
            'gender': data.get('gender'),
            'religion': data.get('religion'),
            'caste': data.get('caste'),
            'profession': data.get('profession'),
            'education': data.get('education'),
        }

        for field, value in category_fields.items():
            if value and not CategoryValue.objects.filter(
                category_id__category_name__iexact=field, category_value__iexact=value
            ).exists():
                raise serializers.ValidationError({field: f"'{value}' is not a valid {field} option."})

        return data
