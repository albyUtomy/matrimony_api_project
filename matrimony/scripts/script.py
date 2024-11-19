from app_user_authentications.models import UserSetupModel

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

def generate_jwt_token(user):
    """
    Generate JWT access and refresh tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return access_token, str(refresh)

def regenerate_tokens_for_all_users():
    """
    Regenerate JWT tokens for all users in the system.
    """
    users = UserSetupModel.objects.all()  # Fetch all users
    for user in users:
        access_token, refresh_token = generate_jwt_token(user)
        print(f"User ID: {user.user_id}")
        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")
        print("-" * 50)


# def blacklist_all_tokens():
#     # Get all refresh tokens for all users
#     refresh_tokens = RefreshToken.objects.all()  # Only works if RefreshToken is stored somehow, or just blacklist known tokens
    
#     # Blacklist each token
#     for token in refresh_tokens:
#         token.blacklist()

#     return "All refresh tokens have been blacklisted."

# # Example of blacklisting a specific token (if you have one):
# def blacklist_token(refresh_token: RefreshToken):
#     refresh_token.blacklist()
#     return "Token has been blacklisted."


def blacklist_all_tokens():
    # Fetch all outstanding tokens
    tokens = OutstandingToken.objects.all()

    for token in tokens:
        try:
            # Blacklist each token
            BlacklistedToken.objects.get_or_create(token=token)
        except Exception as e:
            print(f"Token {token.jti} could not be blacklisted: {e}")

    return "All tokens have been blacklisted."

def run():
    """
    Main function to run the token regeneration process.
    """
    # regenerate_tokens_for_all_users()
    blacklist_all_tokens()