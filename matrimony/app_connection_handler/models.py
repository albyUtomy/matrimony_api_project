from django.db import models

class FriendRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    BLOCKED = 'blocked'
    PENDING = 'pending'

    STATUS_CHOICES = [
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (BLOCKED, 'Blocked'),
        (PENDING, 'Pending'),
    ]
    
    sender = models.ForeignKey('app_user_authentications.UserSetupModel', on_delete=models.CASCADE, related_name='sent_friend_requests')
    recipient = models.ForeignKey('app_user_authentications.UserSetupModel', on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=SENT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'recipient')

    def __str__(self):
        return f"Friend request from {self.sender} to {self.recipient} ({self.status})"


class BlockedUser(models.Model):
    blocker = models.ForeignKey('app_user_authentications.UserSetupModel', on_delete=models.CASCADE, related_name='blockers')
    blocked = models.ForeignKey('app_user_authentications.UserSetupModel', on_delete=models.CASCADE, related_name='blocked_by_connection', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"
