from django.contrib import admin
from apps.meals.models.meals import Meal, MealItem

class MealItemInline(admin.TabularInline):
    model = MealItem
    fields = (
        "product",
        "quantity",
    )
    raw_id_fields = (
        "product",
    )


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "protein",
        "carbs",
        "fat",
        "total_calories",
        "category",
        "date_of_eating",
    )
    inlines = (MealItemInline,)
