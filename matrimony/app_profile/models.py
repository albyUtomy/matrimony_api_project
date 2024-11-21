from django.db import models
from app_admin.models import CategoryValue
from django.core.exceptions import ValidationError

from core.validator import validate_phone_number

# Create your models here.
class UserProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("app_user_authentications.UserSetupModel",on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, 
                                validators=[validate_phone_number],
                                help_text="Enter a valid phone number",
                                unique=True
                                )
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    religion = models.CharField(max_length=50)
    caste = models.CharField(max_length=50)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    profession = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


    def clean(self):
        """
        Validate category-based fields using the CategoryValue table.
        """
        category_fields = {
            'gender': self.gender,
            'religion': self.religion,
            'caste': self.caste,
            'profession': self.profession,
            'education': self.education,
        }

        for field, value in category_fields.items():
            if not CategoryValue.objects.filter(category_id__category_name__iexact=field, category_value__iexact=value).exists():
                raise ValidationError({field: f"'{value}' is not a valid option for {field}."})
            
    def save(self,*args, **kwargs):
        # Update the user's profile field automatically
        super(UserProfile, self).save(*args, **kwargs)
        self.user.profile_id = self
        self.user.save()


    def __str__(self):
        return f"Profile for {self.user.username}"