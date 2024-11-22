from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.field_validator import get_valid_category_values


# Create your models here.

class UserPreference(models.Model):
    user = models.OneToOneField(
        'app_user_authentications.UserSetupModel',
        on_delete=models.CASCADE,
        related_name='preference'
    )
    caste = models.CharField(max_length=50, null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)


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
    is_active = models.BooleanField()

    def clean(self):
        """
        Validate the fields based on the valid category values.
        """
        valid_values = {
            "Caste": get_valid_category_values("Caste"),
            "Profession": get_valid_category_values("Profession"),
            "Education": get_valid_category_values("Education"),
            "Religion": get_valid_category_values("Religion"),
            "Marital_status": get_valid_category_values("Marital_status"),
            "Gender": get_valid_category_values("Gender"),
            "Location": get_valid_category_values("Location"),
        }

        # Validate fields against their valid values
        for field, valid_list in valid_values.items():
            field_value = getattr(self, field.lower(), None)
            if field_value and field_value not in valid_list:
                raise ValidationError({
                    field.lower(): f"Invalid {field.lower()}. Allowed values are: {', '.join(valid_list)}"
                })
            

        # Validate age range
        if self.age_min and self.age_max and self.age_min > self.age_max:
            raise ValidationError({
                'age_min': "Minimum age cannot be greater than maximum age.",
                'age_max': "Maximum age cannot be less than minimum age."
            })
        
        # Validate income range
        if self.income_min and self.income_max and self.income_min > self.income_max:
            raise ValidationError({
                'income_min': "Minimum income cannot be greater than maximum income.",
                'income_max': "Maximum income cannot be less than minimum income."
            })

    def __str__(self):
        return f"Preferences for {self.user.username}"