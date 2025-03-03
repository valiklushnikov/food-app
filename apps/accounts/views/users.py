from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.accounts.serializers.api import users as user_serializers

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary="Register user", tags=["Authentication & Authorization"]
    ),
)
class RegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = user_serializers.RegistrationSerializer


@extend_schema_view(
    post=extend_schema(
        request=user_serializers.ChangePasswordSerializer,
        summary="Сhange password",
        tags=["Authentication & Authorization"],
    ),
)
class ChangePasswordView(APIView):
    def post(self, request):
        user = request.user
        serializer = user_serializers.ChangePasswordSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(summary="Users profile", tags=["Users"]),
)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.UserListSerializer


@extend_schema_view(
    get=extend_schema(summary="User profile", tags=["Users"]),
    patch=extend_schema(summary="Change user profile", tags=["Users"]),
)
class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = user_serializers.MeRetrieveSerializer
    http_method_names = ("get", "patch")

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return user_serializers.MeUpdateSerializer
        return user_serializers.MeRetrieveSerializer

    def get_object(self):
        return self.request.user
