from django.core.exceptions import ValidationError
from app_admin.models import CategoryValue


def validate_category_fields(field_name, value):
    if not CategoryValue.objects.filter(
        category_id__category_name_iexact=field_name,
        category_value__iexact=value
    ).exists():
        raise ValidationError(f"'{value}' is not a valid option for {field_name}.")