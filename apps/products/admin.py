from django.contrib import admin
from apps.products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
            "name",
            "protein",
            "carbs",
            "fat",
            "calories",
            "fatsecret_id",
    )
