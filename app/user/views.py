import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import filters, status, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .utils import IsAdmin, is_admin_user
from .serializers import (
    CreateUserSerializer,
    CustomObtainTokenPairSerializer,
    ListUserSerializer, TokenDecodeSerializer,
    UpdateUserSerializer, PasswordChangeSerializer)


class CustomObtainTokenPairView(TokenObtainPairView):
    """Authentice with email and password"""
    serializer_class = CustomObtainTokenPairSerializer


class PasswordChangeView(viewsets.GenericViewSet):
    '''Allows password change to authenticated user.'''
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        context = {"request": request}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Your password has been updated."}, status.HTTP_200_OK)


class UserViewsets(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ListUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["email", "firstname", "lastname"]
    ordering_fields = [
        "created_at",
        "email",
        "firstname",
        "lastname",
    ]

    def get_queryset(self):
        user: User = self.request.user
        if is_admin_user(user):
            return super().get_queryset().all()
        return super().get_queryset().filter(id=user.id)

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CreateUserSerializer
        if self.action in ["partial_update", "update"]:
            return UpdateUserSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["create"]:
            permission_classes = [AllowAny]
        elif self.action in ["list", "retrieve", "partial_update", "update"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["destroy"]:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class TokenDecode(APIView):
    serializer_class = TokenDecodeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('token', None)
        if token:
            try:
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms="HS256")
            except Exception as err:

                raise AuthenticationFailed(F'Unauthenticated: {err}')

            user = User.objects.get(id=payload['user_id'])
            serializer = ListUserSerializer(instance=user)
            return Response(
                {**serializer.data, "permissions": user.permission_list()})

        raise AuthenticationFailed('Unauthenticated')
