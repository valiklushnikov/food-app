from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken


class CookiesJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return None
        try:
            validated_token = self.get_validated_token(access_token)
        except InvalidToken:
            if refresh_token:
                try:
                    refresh = RefreshToken(refresh_token)
                    new_access_token = str(refresh.access_token)
                    request._request._new_access_token = new_access_token
                    validated_token = self.get_validated_token(new_access_token)
                except InvalidToken:
                    raise AuthenticationFailed("Invalid refresh token")
            else:
                raise AuthenticationFailed(
                    "Access token expired and no refresh token provided"
                )
        try:
            user = self.get_user(validated_token)
        except AuthenticationFailed:
            return None
        return (user, validated_token)
