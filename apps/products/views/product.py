import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from apps.products.models import Product
from apps.products.serializers.api.product import (
    ProductSerializer,
    ProductListSerializer,
)
from apps.products.services import FatSecretAPI


@extend_schema_view(
    get=extend_schema(
        request=ProductSerializer,
        summary="Get product",
        tags=["Products"],
    ),
)
class ProductView(APIView):
    def get(self, request, product_id):
        fatsecret_api = FatSecretAPI()
        if Product.objects.filter(fatsecret_id=product_id).exists():
            product = Product.objects.get(fatsecret_id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            response_data = fatsecret_api.get_product(product_id)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            fatsecret_id = response_data["food_id"]
            name = response_data["food_name"]
            protein = response_data["servings"]["serving"][0]["protein"]
            carbs = response_data["servings"]["serving"][0]["carbohydrate"]
            fat = response_data["servings"]["serving"][0]["fat"]
            calories = response_data["servings"]["serving"][0]["calories"]
        except KeyError as e:
            return Response({"error": f"Key {e} does not exist"})

        product_data = {
            "fatsecret_id": fatsecret_id,
            "name": name,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "calories": calories,
        }
        serializer = ProductSerializer(data=product_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Product name",
                required=False,
                type=OpenApiTypes.STR,
            )
        ],
        summary="Search product",
        tags=["Products"],
    )
)
class ProductSearchView(APIView):
    def get(self, request):
        fatsecret_api = FatSecretAPI()
        name = request.GET.get("name")
        try:
            response_data = fatsecret_api.search_products(name)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        products = [
            {
                "fatsecret_id": item["food_id"],
                "name": item["food_name"],
                "food_description": item["food_description"],
            }
            for item in response_data
        ]
        serializer = ProductListSerializer(data=products, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
