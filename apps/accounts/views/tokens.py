from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response


User = get_user_model()

def set_auth_cookies(response, access_token=None, refresh_token=None):
    if access_token:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )
    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )

    return response


@extend_schema_view(
    post=extend_schema(summary="Obtain token", tags=["Authentication & Authorization"]),
)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            email = request.data["email"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User does not exist"})

            auth_response = Response()

            auth_response.data = {
                "success": True,
                "user": {
                    "email": user.email,
                },
            }

            return set_auth_cookies(auth_response, access_token, refresh_token)
        except:
            return Response({"success": False})


@extend_schema_view(
    post=extend_schema(
        summary="Refresh token", tags=["Authentication & Authorization"]
    ),
)
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"success": False, "error": "No refresh token"})

        request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)
        access_token = response.data.get("access")

        if not access_token:
            return Response({"success": False, "error": "Invalid token"})

        auth_response = Response({"success": True})

        return set_auth_cookies(auth_response, access_token)
