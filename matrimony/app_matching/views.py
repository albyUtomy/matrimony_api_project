# app_matching/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_user_authentications.models import UserSetupModel
from app_preference.models import UserPreference
from .models import Matching, MatchDetail

class UserMatchesAPIView(APIView):
    def calculate_and_save_matches(self, user):
        try:
            # Retrieve the user's preferences
            preference = UserPreference.objects.get(user=user)
        except UserPreference.DoesNotExist:
            return {"error": "User preferences not found"}, status.HTTP_404_NOT_FOUND

        # Exclude the current user from matching
        other_users = UserSetupModel.objects.exclude(user_id=user.user_id)
        matches = []

        for other_user in other_users:
            # Skip users without a profile
            if not hasattr(other_user, 'profile') or other_user.profile is None:
                continue

            # Calculate the match score
            score = 0

            # Match criteria
            if preference.age_min and preference.age_max:
                if other_user.profile.age and preference.age_min <= other_user.profile.age <= preference.age_max:
                    score += 1

            if preference.height_min and preference.height_max:
                if other_user.profile.height and preference.height_min <= other_user.profile.height <= preference.height_max:
                    score += 1

            if preference.profession and other_user.profile.profession:
                if other_user.profile.profession.lower() == preference.profession.lower():
                    score += 1

            if preference.caste and other_user.profile.caste:
                if other_user.profile.caste.lower() == preference.caste.lower():
                    score += 1

            if preference.education and other_user.profile.education:
                if other_user.profile.education.lower() == preference.education.lower():
                    score += 1

            if preference.language and other_user.profile.language:
                if other_user.profile.language.lower() == preference.language.lower():
                    score += 1

            if preference.religion and other_user.profile.religion:
                if other_user.profile.religion.lower() == preference.religion.lower():
                    score += 1

            if preference.gender and other_user.profile.gender:
                if other_user.profile.gender.lower() == preference.gender.lower():
                    score += 1

            if preference.marital_status and other_user.profile.marital_status:
                if other_user.profile.marital_status.lower() == preference.marital_status.lower():
                    score += 1

            if preference.location and other_user.profile.location:
                if other_user.profile.location.lower() == preference.location.lower():
                    score += 1

            # Save matches with a score above 5
            if score > 3:
                # Create or get the Matching instance
                matching, created = Matching.objects.get_or_create(user=user)

                # Check if the match already exists to prevent duplicate entries
                existing_match = MatchDetail.objects.filter(matching=matching, matched_user=other_user).first()
                
                if not existing_match:
                    # Create a new MatchDetail if it doesn't exist
                    MatchDetail.objects.create(
                        matching=matching,
                        matched_user=other_user,
                        score=score
                    )

                matches.append({
                    "matched_user_id": other_user.user_id,
                    "name":other_user.username,
                    "score": score,
                })

        return matches

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = UserSetupModel.objects.get(user_id=user_id)
        except UserSetupModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        matches = self.calculate_and_save_matches(user)

        if isinstance(matches, tuple) and matches[1] != status.HTTP_200_OK:
            return Response({"error": matches[0]["error"]}, status=matches[1])

        return Response(
            {"user_id": user_id, "matches": matches},
            status=status.HTTP_200_OK
        )
