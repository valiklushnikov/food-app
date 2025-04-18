from rest_framework import serializers
from apps.meals.models.meals import Meal, MealItem
from apps.meals.serializers.nested.meal_item import MealItemSerializer, MealItemDetailSerializer
from apps.meals.services import create_meal, add_product_to_meal


class BaseMealSerializer(serializers.ModelSerializer):
    meal_category = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_meal_category(self, obj):
        return obj.get_category_display()


class BaseMealWriteSerializer(BaseMealSerializer):
    product = MealItemSerializer(write_only=True)
    protein = serializers.FloatField(read_only=True)
    carbs = serializers.FloatField(read_only=True)
    fat = serializers.FloatField(read_only=True)
    total_calories = serializers.FloatField(read_only=True)
    food = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_food(self, obj):
        meal_items = MealItem.objects.filter(meal=obj)
        return [MealItemDetailSerializer(meal_item).data for meal_item in meal_items]

class BaseMealReadSerializer(BaseMealSerializer):
    products = MealItemDetailSerializer(read_only=True, many=True, source="items")

    class Meta:
        abstract = True

class MealCreateSerializer(BaseMealWriteSerializer):
    category = serializers.ChoiceField(choices=Meal.CategoryChoices.choices, write_only=True)

    class Meta:
        model = Meal
        fields = (
            "id",
            "meal_category",
            "category",
            "protein",
            "carbs",
            "fat",
            "total_calories",
            "product",
            "food",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        category = validated_data.get("category")
        product_data = validated_data.get("product")
        return create_meal(user, category, product_data)


class MealUpdateSerializer(BaseMealWriteSerializer):

    class Meta:
        model = Meal
        fields = (
            "id",
            "meal_category",
            "protein",
            "carbs",
            "fat",
            "total_calories",
            "product",
            "food",
        )

    def update(self, instance, validated_data):
        product_data = validated_data.get("product")
        add_product_to_meal(instance, product_data)
        return instance


class MealDisplaySerializer(BaseMealReadSerializer):
    user = serializers.CharField(source="user.email")

    class Meta:
        model = Meal
        fields = (
            "id",
            "user",
            "protein",
            "carbs",
            "fat",
            "total_calories",
            "date_of_eating",
            "meal_category",
            "products"
        )
