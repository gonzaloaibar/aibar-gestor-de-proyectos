from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


User=get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'},
                                     validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        read_only_fields = ('id',)

    def validate_email(self, email):
        email=email.strip().lower()#normaliza a minuscula y elimina espacios en blanco
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id','email','date_joined',)