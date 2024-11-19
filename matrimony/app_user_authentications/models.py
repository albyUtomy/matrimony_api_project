# django import
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import now

# other imports
from .validators import validate_phone_number, password_validate


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
    date_joined = models.DateTimeField(auto_now=True)
    subscription_id = models.IntegerField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # managers
    # admin_object = AdminManager()
    # user_object = UserManager()
    active_object = ActiveManager()
    inactive_object = InActiveManger()

    # default manager
    objects = models.Manager()

    def __str__(self):
        return f'{self.username} - id : {self.user_id}'
    


"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RefreshTokenStore(models.Model):
    user = models.ForeignKey(UserSetupModel, on_delete=models.CASCADE, related_name="refresh_tokens")
    token = models.CharField(max_length=225)
    token_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.token and  not self.token_hash.startswith('pbkdf2_'):  # Avoid re-hashing
            self.token_hash = make_password(self.token)
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.is_active and self.expires_at > now()
    
    def verify_token(self, token):
        return self.is_valid() and check_password(token, self.token_hash)
    
    def __str__(self):
        return f"Token for user {self.user.username}, active : {self.is_active}"
"""