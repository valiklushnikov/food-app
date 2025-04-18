from rest_framework import serializers
from apps.accounts.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="get_gender_display")
    activity_level = serializers.CharField(source="get_activity_level_display")
    goal = serializers.CharField(source="get_goal_display")

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
        choices_values = [
            choice[0] for choice in Profile._meta.get_field("activity_level").choices
        ]
        if value not in choices_values:
            raise serializers.ValidationError(
                f"Invalid activity level value. Valid value: {', '.join([str(choice) for choice in choices_values])}"
            )
        return value


class ProfileSummarizeSerializer(serializers.ModelSerializer):
    macros = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "recommended_calories",
            "macros",
        )

    def get_macros(self, obj):
        macros = {}
        match obj.get_goal_display():
            case "Weight loss":
                macros["protein"] = obj.weight * 2
                macros["fat"] = round(
                    obj.weight * 0.8
                    if obj.get_gender_display() == "Male"
                    else obj.weight * 1.2
                )
            case "Weight maintenance":
                macros["protein"] = round(obj.weight * 1.5)
                macros["fat"] = obj.weight * 1
            case "Weight gain":
                macros["protein"] = round(obj.weight * 1.8)
                macros["fat"] = round(obj.weight * 1.2)
        macros["carbs"] = round(
            (
                obj.recommended_calories
                - (macros.get("protein") * 4 + macros.get("fat") * 9)
            ) / 4
        )
        return macros
