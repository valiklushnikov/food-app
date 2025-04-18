from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.meals.serializers.api import meals
from apps.meals.serializers.nested import meal_item
from apps.meals.models.meals import Meal, MealItem
from apps.meals import backends as meal_filter
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)


@extend_schema_view(
    list=extend_schema(
        summary="Meals list",
        tags=["Meals"],
        parameters=[
            OpenApiParameter(
                name="from_date",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by date (format: YYYY-MM-DD)",
                required=False,
            ),
            OpenApiParameter(
                name="to_date",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by date (format: YYYY-MM-DD)",
                required=False,
            )
        ],
    ),
    retrieve=extend_schema(summary="Meal detail", tags=["Meals"]),
    create=extend_schema(summary="Create meal", tags=["Meals"]),
    update=extend_schema(summary="Update meal", tags=["Meals"]),
    partial_update=extend_schema(exclude=True),
)
class MealsViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Meal.objects.prefetch_related("items__product").all()
    serializer_class = meals.MealDisplaySerializer
    filter_backends = (
        meal_filter.IsOwnerFilterBackend,
        meal_filter.MealDateFilterBackend,
    )

    def get_serializer_class(self):
        if self.action == "create":
            return meals.MealCreateSerializer
        if self.action == "update":
            return meals.MealUpdateSerializer
        return self.serializer_class


@extend_schema_view(
    list=extend_schema(summary="Meal product list", tags=["Meals Products"], operation_id="list_meal_products"),
    retrieve=extend_schema(summary="Meal product detail", tags=["Meals Products"], operation_id="retrieve_meal_product"),
    destroy=extend_schema(summary="Delete meal product", tags=["Meals Products"]),
    increase_product=extend_schema(
        summary="Increase meal product", tags=["Meals Products"]
    ),
    decrease_product=extend_schema(
        summary="Decrease meal product", tags=["Meals Products"]
    ),
    quantity_product=extend_schema(
        summary="Change meal product quantity", tags=["Meals Products"]
    ),
)
class MealProductViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    queryset = MealItem.objects.select_related("product").all()
    serializer_class = meal_item.MealItemDetailSerializer
    lookup_url_kwarg = "product_id"
    lookup_field = "product__fatsecret_id"

    def get_queryset(self):
        return super().get_queryset().filter(meal_id=self.kwargs.get("pk"))

    def get_serializer_class(self):
        if self.action == "create":
            return meal_item.MealItemCreateSerializer
        return self.serializer_class

    @action(
        methods=["POST"],
        detail=True,
        url_path="decrease",
        serializer_class=None
    )
    def decrease_product(self, request, pk=None, product_id=None):
        meal_item = get_object_or_404(
            MealItem,
            meal_id=pk,
            product__fatsecret_id=product_id
        )
        meal_item.quantity = max(0, meal_item.quantity - 10)
        if meal_item.quantity == 0:
            meal_item.delete()
            return Response({"message": "Product removed"})
        meal_item.save()
        return Response(
            {"message": "Quantity decreased", "quantity": meal_item.quantity},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="increase",
        serializer_class=None
    )
    def increase_product(self, request, pk=None, product_id=None):
        meal_item = get_object_or_404(
            MealItem,
            meal_id=pk,
            product__fatsecret_id=product_id
        )
        meal_item.quantity = meal_item.quantity + 10
        meal_item.save()
        return Response(
            {"message": "Quantity increased", "quantity": meal_item.quantity},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["PATCH"],
        detail=True,
        url_path="change-quantity",
        serializer_class=None
    )
    def quantity_product(self, request, pk=None, product_id=None):
        meal_item = get_object_or_404(
            MealItem,
            meal_id=pk,
            product__fatsecret_id=product_id
        )
        request_quantity = request.data.get("quantity", meal_item.quantity)
        meal_item.quantity = max(0, request_quantity)
        if meal_item.quantity == 0:
            meal_item.delete()
            return Response({"message": "Product removed"})
        meal_item.save()
        return Response(
            {"message": "Quantity changed", "quantity": meal_item.quantity},
            status=status.HTTP_200_OK,
        )
