# app_matching/models.py
from django.db import models
from app_user_authentications.models import UserSetupModel

class Matching(models.Model):
    user = models.ForeignKey(
        UserSetupModel, on_delete=models.CASCADE, related_name='matches_initiated'
    )
    matched_users = models.ManyToManyField(
        UserSetupModel, through='MatchDetail', related_name='matches_received'
    )

class MatchDetail(models.Model):
    matching = models.ForeignKey(Matching, on_delete=models.CASCADE)
    matched_user = models.ForeignKey(UserSetupModel, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('matching', 'matched_user')  # Ensure no duplicate matches
