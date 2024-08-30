from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    '''
    Signup serializer to format the signup data.
    '''
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(SignUpSerializer, self).create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
