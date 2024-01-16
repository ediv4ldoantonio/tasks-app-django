from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        options = {"hours": settings.TOKEN_LIFESPAN}
        refresh = self.get_token(self.user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(**options))
        self.user.save_last_login()
        data['refresh'] = str(refresh)
        data['access'] = str(access_token)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token.id = user.id
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token["email"] = user.email
        return token


class TokenDecodeSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "firstname",
            "lastname",
            "email",
            "created_at",
            "is_admin",
        ]

    def to_representation(self, instance):
        return super().to_representation(instance)
    

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=False)
    new_password = serializers.CharField(max_length=128, min_length=5)

    def validate_old_password(self, value):
        request = self.context["request"]

        if not request.user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self):
        user: User = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save(update_fields=["password"])


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "firstname",
            "lastname",
        ]

    def update(self, instance, validated_data):
        """ Prevent user from updating password """
        if validated_data.get("password", False):
            validated_data.pop('password')
        instance = super().update(instance, validated_data)

        return instance


class BasicUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "firstname",
            "lastname",
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    """ Serializer for creating user object """

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "firstname",
            "lastname",
            "password",
        )

        extra_kwargs = {
            "firstname": {"required": True},
            "lastname": {"required": True},
            "password": {"required": True, "write_only": True},
        }


    def validate_email(self, value):
        if value:
            email = value.lower().strip()
            if get_user_model().objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {'email': 'Email already exists'})
        return value

    @transaction.atomic
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = User.objects.create(**validated_data)
        return user
