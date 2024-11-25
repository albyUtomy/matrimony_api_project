# django import
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from app_connection_handler.models import BlockedUser

# other imports
from core.validator import validate_phone_number

# Custom Managers
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
    def get_by_natural_key(self, username):
        return self.get(username=username)
    

class InActiveManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


# class AdminManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_admin=True)

#     def get_by_natural_key(self, username):
#         return self.get(username=username)


# class UserManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_admin=False)
    
#     def get_by_natural_key(self, username):
#         return self.get(username=username)


# Create your models here.
class UserSetupModel(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    phone_no = models.CharField(max_length=10, 
                                validators=[validate_phone_number],
                                help_text="Enter a valid phone number",
                                unique=True
                                )
    email = models.EmailField(unique=True, blank=False, null=False)
    profile = models.OneToOneField('app_profile.UserProfile',on_delete=models.SET_NULL,null=True, blank=True)
    preference = models.OneToOneField('app_preference.UserPreference',on_delete=models.SET_NULL,null=True, blank=True, related_name='user_preference')
    date_joined = models.DateTimeField(auto_now=True)
    subscription_id = models.IntegerField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    blocked_users = models.ManyToManyField('self', symmetrical=False, related_name='blocked_by_users', blank=True)

    # managers
    # admin_object = AdminManager()
    # user_object = UserManager()
    active_object = ActiveManager()
    inactive_object = InActiveManger()

    # default manager
    objects = models.Manager()

    def __str__(self):
        return f'{self.username} - id : {self.user_id}'
    
