from app_admin.models import CategoryValue

def add_primaryKey():
    total_category = CategoryValue.objects.all()
    print(total_category)

def run():
    """
    Main function to run the token regeneration process.
    """
    # regenerate_tokens_for_all_users()
    add_primaryKey()