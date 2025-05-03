from django.urls import path
from apps.accounts.views import users, tokens


urlpatterns = [
    path("users/", users.UserListView.as_view(), name="user-list"),
    path("users/register/", users.RegistrationView.as_view(), name="register"),
    path("users/me/", users.MeView.as_view(), name="me"),
    path("users/summary/", users.SummaryView.as_view(), name="summary"),
    path(
        "users/change-password/",
        users.ChangePasswordView.as_view(),
        name="change_password",
    ),
    path(
        "users/token/",
        tokens.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "users/token/refresh/",
        tokens.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
