from app_admin.models import CategoryValue, Subscription, Category
from app_user_authentications.models import UserSetupModel
from app_profile.models import UserProfile
import random

def add_primaryKey():
    total_category = CategoryValue.objects.all()
    print(total_category)

def random_subscription():
    total_subscription = Subscription.objects.values_list('subscription_id', flat=True)
    list_subscription_ids = list(total_subscription)
    print(list_subscription_ids)

    users = UserSetupModel.objects.all()
    import random
    for user in users:
        random_subscription_id = random.choice(list_subscription_ids)
        user.subscription_id = random_subscription_id
        user.save()
        print(f"{random_subscription_id} is assigned to user {user.username}")

def random_location():
    # Get the 'Location' category
    location_category = Category.objects.filter(category_name='Location').first()

    if location_category:
        # Get all category values related to 'Location'
        total_location = CategoryValue.objects.filter(category_id=location_category).values_list('category_value', flat=True)
        
        # Convert to a list and print
        list_location = list(total_location)
        
        if list_location:
            # Assign a random location to each user profile
            user_profiles = UserProfile.objects.all()  # You can filter as needed (e.g., active profiles)
            
            for profile in user_profiles:
                # Randomly select a location for each user profile
                random_location = random.choice(list_location)
                profile.location = random_location  # Assign the random location to the profile
                profile.save()
                print(f"Assigned location '{random_location}' to user profile {profile.user.username}")
        else:
            print("No locations available to assign.")
    else:
        print("Location category not found.")

def run():
    """
    Main function to run the token regeneration process.
    """
    # regenerate_tokens_for_all_users()
    # random_subscription()
    random_location()