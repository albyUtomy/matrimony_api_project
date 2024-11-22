from app_admin.models import CategoryValue

def get_valid_category_values(category_name):
    """
    Fetch valid values for a given category name from CategoryValue.
    """
    valid_values =  CategoryValue.objects.filter(category_id__category_name=category_name).values_list("value", flat=True)
    if not valid_values.exists():
        raise ValueError(f"No valid filed found : {category_name}")
    
    return list(valid_values)