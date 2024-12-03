from .models import UserSetupModel
from app_user_history.models import TokenStorage
from app_matching.models import Matching
from app_notification.models import Notification
from app_message.models import Message
from rest_framework_simplejwt.tokens import RefreshToken


def deactivate_user(user_to_deactivate, user_id, refresh_token):
    user_to_deactivate.profile.is_active = False
    user_to_deactivate.profile.save()
    user_to_deactivate.preference.is_active = False
    user_to_deactivate.preference.save()
    TokenStorage.objects.filter(user_id=user_id).update(access_token_active=False, refresh_token_active=False)
    Matching.objects.filter(user=user_id).update(is_active=False)
    Notification.objects.filter(user=user_id).update(is_active=False)
    Message.objects.filter(sender=user_id).update(is_active=False)
    UserSetupModel.objects.filter(user_id=user_id).update(is_active=False)

    

    token = RefreshToken(refresh_token)
    token.blacklist()