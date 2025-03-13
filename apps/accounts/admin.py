from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from apps.accounts.models.users import User
from apps.accounts.models.profile import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "age",
        "gender",
        "user",
    )


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password",
                    "password2",
                ),
            },
        ),
    )
    list_display = (
        "id",
        "email",
        "last_login",
    )

    list_display_links = ("email",)
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email",)
    ordering = ("-email",)
    readonly_fields = ("last_login",)
