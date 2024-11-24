from django.db import models

# Create your models here.

class Matching(models.Model):
    user = models.OneToOneField(
        'app_user_authentications.UserSetupModel',
        on_delete=models.CASCADE,
        related_name='matching'
    )
    matched_users = models.ManyToManyField(
        'app_user_authentications.UserSetupModel',
        related_name='matched_with'
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)