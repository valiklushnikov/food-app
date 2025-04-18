import os
import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
import apps.accounts.constants as const


def image_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join(f"uploads/profiles/{instance.user}", filename)


class Profile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GenderChoices.choices, default=GenderChoices.FEMALE
    )
    weight = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    activity_level = models.FloatField(
        choices=const.ACTIVITY_LEVEL_CHOICES, default=const.LOW
    )
    goal = models.SmallIntegerField(
        choices=const.GOAL_CHOICES, default=const.WEIGHT_MAINTENANCE_KCAL
    )
    recommended_calories = models.PositiveSmallIntegerField(default=2000, blank=True)
    photo = models.ImageField(upload_to=image_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def calculate_bmr(self):
        return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + (5 if self.gender == "M" else -161)

    @property
    def calculate_tdee(self):
        return self.calculate_bmr * self.activity_level

@receiver(post_save, sender=Profile)
def update_recommended_calories(sender, instance, created, **kwargs):
    Profile.objects.filter(id=instance.id).update(recommended_calories=instance.calculate_tdee)

