from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.meals.views import meals


router = DefaultRouter()


router.register(r"(?P<pk>\d+)/products", meals.MealProductViewSet, "products")
router.register(r"", meals.MealsViewSet, basename="meals")

urlpatterns = [
    path("meals/", include(router.urls)),
]
