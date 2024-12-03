from django.db import models
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey('app_user_authentications.UserSetupModel', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('app_user_authentications.UserSetupModel', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, default='unseen', choices=[('unseen', 'Unseen'), ('seen', 'Seen')])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"

    def mark_as_read(self):
        """Method to mark the message as read and update the read_at timestamp and status."""
        if not self.read_at:
            self.read_at = timezone.now()
            self.status = 'seen'
            self.save()

    class Meta:
        ordering = ['-created_at']
