from apps.meals.models.meals import Meal, MealItem


def create_meal(user, category, product_data):
    meal = Meal.objects.create(user=user, category=category)
    MealItem.objects.create(
        meal=meal, product=product_data["product"], quantity=product_data["quantity"]
    )
    meal.update_nutrient()
    return meal


def add_product_to_meal(meal, product_data):
    meal_item, created = MealItem.objects.get_or_create(
        meal=meal,
        product=product_data["product"],
        defaults={"quantity": product_data["quantity"]},
    )
    if not created:
        meal_item.quantity += product_data["quantity"]
        meal_item.save()
    meal.refresh_from_db()
    meal.update_nutrient()
