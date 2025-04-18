from rest_framework import serializers
from apps.accounts.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    activity_level = serializers.SerializerMethodField()

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

    def get_activity_level(self, obj):
        return obj.get_activity_level_display()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    gender = serializers.CharField()
    activity_level = serializers.FloatField()

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

    def validate_activity_level(self, value):
        choices_values = [choice[0] for choice in Profile._meta.get_field("activity_level").choices]
        if value not in choices_values:
            raise serializers.ValidationError(
                f"Invalid activity level value. Valid value: {', '.join([str(choice) for choice in choices_values])}"
            )
        return value
