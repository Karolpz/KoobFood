from ..models import CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'password', 'confirm_password']
        read_only_fields = ['id'] 

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Les mots de passe ne correspondent pas."}
            )
        data.pop('confirm_password')

        return data

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)