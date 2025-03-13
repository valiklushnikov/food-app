from rest_framework import serializers
from apps.accounts.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "age",
            "gender",
            "weight",
            "height",
            "activity_level",
            "goal",
            "photo",
            "created_at",
        )

    def get_gender(self, obj):
        return obj.get_gender_display()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    gender = serializers.CharField()

    class Meta:
        model = Profile
        fields = (
            "age",
            "gender",
            "weight",
            "height",
            "activity_level",
            "goal",
            "photo",
        )

    def validate_gender(self, value):
        value = value.upper()
        if value not in Profile.GenderChoices.values:
            raise serializers.ValidationError(
                f"Invalid gender value. Valid value: {", ".join(Profile.GenderChoices.values)}"
            )
        return value
