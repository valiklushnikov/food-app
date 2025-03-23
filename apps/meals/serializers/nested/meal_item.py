from rest_framework import serializers
from apps.products.models.products import Product
from apps.meals.models.meals import MealItem
from apps.products.serializers.api.products import ProductSerializer
from apps.products import services


class MealItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.SlugRelatedField(
        write_only=True,
        source="product",
        queryset=Product.objects.all(),
        slug_field="fatsecret_id",
    )


    class Meta:
        model = MealItem
        fields = (
            "product",
            "product_id",
            "quantity",
        )

    def to_internal_value(self, data):
        fatsecret_id = data.get("product_id")
        if Product.objects.filter(fatsecret_id=fatsecret_id).exists():
            product = Product.objects.filter(fatsecret_id=fatsecret_id).first()
        else:
            try:
                product_data = services.retrieve_product_from_fatsecret_api(fatsecret_id)
            except ValueError as error:
                raise serializers.ValidationError({"error": error})
            serializer = ProductSerializer(data=product_data)
            serializer.is_valid(raise_exception=True)
            product = serializer.save()
        data["product"] = product
        return super().to_internal_value(data)



class MealItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    protein = serializers.SerializerMethodField()
    carbs = serializers.SerializerMethodField()
    fat = serializers.SerializerMethodField()
    total_calories = serializers.SerializerMethodField()
    class Meta:
        model = MealItem
        fields = (
            "product",
            "quantity",
            "protein",
            "carbs",
            "fat",
            "total_calories",
        )

    def get_protein(self, obj):
        return round(obj.product.protein * (obj.quantity / 100), 2)

    def get_carbs(self, obj):
        return round(obj.product.carbs * (obj.quantity / 100), 2)

    def get_fat(self, obj):
        return round(obj.product.fat * (obj.quantity / 100), 2)

    def get_total_calories(self, obj):
        return round(obj.product.calories * (obj.quantity / 100), 2)
