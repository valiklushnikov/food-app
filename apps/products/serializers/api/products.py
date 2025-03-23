from rest_framework import serializers
from apps.products.models.products import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "protein",
            "carbs",
            "fat",
            "calories",
            "fatsecret_id",
        )

        def create(self, validated_data):
            return Product.objects.create(**validated_data)


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.Serializer):
    fatsecret_id = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=64)
    food_description = serializers.CharField(max_length=255)
