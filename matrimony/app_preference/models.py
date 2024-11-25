from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.field_validator import get_valid_category_values
from app_admin.models import CategoryValue

# Create your models here.

class UserPreference(models.Model):
    user = models.ForeignKey("app_user_authentications.UserSetupModel",on_delete=models.CASCADE, related_name='preference_user')
    preference_id = models.AutoField(primary_key=True)
    caste = models.CharField(max_length=50, null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    marital_status = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    

    age_min = models.PositiveIntegerField(
        validators=[MinValueValidator(18)],
        help_text="Minimum preferred age.",
        null=True,
        blank=True
    )

    age_max = models.PositiveIntegerField(
        validators=[MinValueValidator(18)],
        help_text="Maximum preferred age.",
        null=True,
        blank=True
    )
    
    height_min = models.PositiveIntegerField(blank=True, null=True)
    height_max = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        """
        Validate category-based fields using the CategoryValue table.
        """
        # Validate category-based fields
        category_fields = {
            'religion':self.religion,
            'gender': self.gender,
            'caste': self.caste,
            'profession': self.profession,
            'education': self.education,
            'language': self.language,
            'marital_status':self.marital_status,
            'location':self.location
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
                
                raise ValidationError({
                    field: f"'{value}' is not a valid {field} option.",
                    "valid_fields": list(valid_values)  # Include valid options in the error
                })
        # Validate age range
        if self.age_min and self.age_max and self.age_min > self.age_max:
            raise ValidationError({
                'age_min': "Minimum age cannot be greater than maximum age.",
                'age_max': "Maximum age cannot be less than minimum age."
            })

        # Validate height range
        if self.height_min and self.height_max and self.height_min > self.height_max:
            raise ValidationError({
                'height_min': "Minimum height cannot be greater than maximum height.",
                'height_max': "Maximum height cannot be less than minimum height."
            })

    def __str__(self):
        return f"Preferences for {self.user.username}"