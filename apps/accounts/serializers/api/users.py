from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.accounts.models.profile import Profile

from apps.accounts.serializers.nested.profile import (
    ProfileSerializer,
    ProfileUpdateSerializer,
)

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password_repeat",
            "first_name",
            "last_name"
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError("Passwords does not match")
        return attrs

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exist")
        return email

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as error:
            raise serializers.ValidationError({"password": error.messages})
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        Profile.objects.create(user=user)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "old_password",
            "new_password"
        )

    def validate(self, attrs):
        user = self.instance
        old_password = attrs.pop("old_password", None)
        if not user.check_password(old_password):
            raise serializers.ValidationError("Incorrect current password")
        return attrs

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as error:
            raise serializers.ValidationError({"password": error.messages})
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("new_password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "profile",
        )


class MeRetrieveSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "profile",
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "profile",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        profile_data = (
            validated_data.pop("profile") if "profile" in validated_data else None
        )
        instance.save()
        if profile_data:
            profile_instance = instance.profile
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)
            profile_instance.save()
        return instance
