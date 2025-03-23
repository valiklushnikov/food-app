from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models.products import Product


User = get_user_model()


class Meal(models.Model):
    class CategoryChoices(models.TextChoices):
        BREAKFAST = "B", "Breakfast"
        LUNCH = "L", "Lunch"
        DINNER = "D", "Dinner"
        SNACK = "S", "Snack"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    total_calories = models.FloatField(default=0)
    category = models.CharField(max_length=1, choices=CategoryChoices.choices)
    date_of_eating = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name="meals", through="MealItem")

    def __str__(self):
        return f"{self.category}: {self.total_calories} - {self.date_of_eating}"

    def update_nutrient(self):
        meal_items = self.items.all()
        self.protein = round(sum(item.product.protein * (item.quantity / 100) for item in meal_items), 2)
        self.carbs = round(sum(item.product.carbs * (item.quantity / 100) for item in meal_items), 2)
        self.fat = round(sum(item.product.fat * (item.quantity / 100) for item in meal_items), 2)
        self.total_calories = round(sum(item.product.calories * (item.quantity / 100) for item in meal_items), 2)
        self.save()


class MealItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="items")
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.product} - {self.quantity} g"
