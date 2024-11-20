from django.db import models



# Create your models here.
class UserProfileModel(models.Model):
    user_id = models.ForeignKey("app_user_authentications.UserSetupModel",on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)