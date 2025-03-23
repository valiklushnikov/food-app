from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    calories = models.FloatField()
    fatsecret_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
