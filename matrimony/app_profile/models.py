from django.db import models



# Create your models here.
class UserProfileModel(models.Model):
    user_id = models.ForeignKey("app_user_authentications.UserSetupModel",on_delete=models.CASCADE)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    religion = models.CharField(max_length=50)