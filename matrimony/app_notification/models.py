from django.db import models

class Notification(models.Model):
    # Possible notification types
    NOTIFICATION_TYPES = (
        ('MATCH', 'User Match'),
        ('MESSAGE', 'New Message'),
        ('BLOCK', 'User Blocked'),
        # Add more notification types as needed
    )
    
    user = models.ForeignKey('app_user_authentications.UserSetupModel', related_name='notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'
