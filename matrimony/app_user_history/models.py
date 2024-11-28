from django.db import models
from django.conf import settings

class TokenStorage(models.Model):
    user = models.ForeignKey('app_user_authentications.UserSetupModel',on_delete=models.CASCADE, 
        related_name='tokens',
        help_text="The user associated with the tokens"
    )
    access_token = models.TextField(help_text="The user's access token")
    refresh_token = models.TextField(help_text="The user's refresh token")
    access_token_active = models.BooleanField(default=True, help_text="State of the access token: Active or Inactive")
    refresh_token_active = models.BooleanField(default=True, help_text="State of the refresh token: Active or Inactive")
    username = models.CharField(max_length=50, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time when the tokens were created")
    updated_at = models.DateTimeField(auto_now=True, help_text="The time when the tokens were last updated")


    def deactivate_access_token(self):
        """Deactivate the access token."""
        self.access_token_active = False
        self.save(update_fields=['access_token_active'])

    def deactivate_refresh_token(self):
        """Deactivate the refresh token."""
        self.refresh_token_active = False
        self.save(update_fields=['refresh_token_active'])

    def save(self, *args, **kwargs):
        self.is_admin = self.user.is_admin
        self.username = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tokens for {self.user.username} (Access Active: {self.access_token_active}, Refresh Active: {self.refresh_token_active})"


    class Meta:
        verbose_name = "Token Storage"
        verbose_name_plural = "Token Storage"
