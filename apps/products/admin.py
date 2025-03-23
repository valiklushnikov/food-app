from django.contrib import admin
from apps.products.models.products import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "name",
            "protein",
            "carbs",
            "fat",
            "calories",
            "fatsecret_id",
    )
