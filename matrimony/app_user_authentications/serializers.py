from rest_framework import serializers
from .models import UserSetupModel
from .validators import password_validate
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserSetupModel
        fields = [
            'user_id', 'username','profile', 'password', 'first_name', 'last_name', 'email', 
            'phone_no', 'is_active', 'is_admin', 'last_login'
        ]
        read_only_fields = ['user_id', 'last_login']


    def validate_password(self, value):
        try:
            return password_validate(value)  
        # This will raise DjangoValidationError if invalid
        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_password = self.validate_password(password)  
    
        # Ensure validated_password is a plain string
        if not isinstance(validated_password, str):
            raise serializers.ValidationError("Password validation failed.")

        user = UserSetupModel(**validated_data)
        user.set_password(validated_password)  # Hash the validated password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
    

class InactiveUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserSetupModel
        fields = ['user_id','full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        return data