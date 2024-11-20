from rest_framework import serializers


from .models import Category, CategoryValue
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']
        
    def validate_category_name(self, value):
        value = value.capitalize()
        if Category.objects.filter(category_name__iexact=value).exists():
            raise serializers.ValidationError(f"A category with the name '{value}' already exists.")
        return value.capitalize()
    


class CategoryValuesSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = 'category_id.category_name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset= Category.objects.all())
    category_values = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True
    )
    class Meta:
        model = CategoryValue
        fields = ['category_id', 'category_name', 'category_values']

    def validate_category_values(self, values):
        capitalized_values = [value.capitalize() for value in values]
        category_id = self.initial_data.get('category_id')

        # Check if the category values already exist in the specified category
        for value in capitalized_values:
            if CategoryValue.objects.filter(category_id=category_id, category_value__iexact=value).exists():
                raise serializers.ValidationError(f"A value with the name '{value}' already exists in this category.")
        
        return capitalized_values
    

class CategoryValueListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category_id.category_name', read_only=True)
    
    class Meta:
        model = CategoryValue
        fields = ['category_id', 'category_name', 'category_value']