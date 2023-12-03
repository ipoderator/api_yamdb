import secrets
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from api.utils import HTTPMethods
from users.serializers import (
    UserSerializer,
    UserSignUpSerializer,
    GetTokenSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Viewet for users."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (
        IsAdmin,
    )
    lookup_field = 'username'
    filter_backends = (
        filters.SearchFilter,
    )
    search_fields = (
        'username',
    )

    @action(
        methods=[HTTPMethods.PATCH, HTTPMethods.GET],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == HTTPMethods.GET:
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view([HTTPMethods.POST])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        user, _ = User.objects.get_or_create(
            username=username, email=email
        )
    except IntegrityError:
        return Response(
            'Проблемы с базой данных.',
            status=status.HTTP_400_BAD_REQUEST
        )
    code = string.ascii_letters + string.digits
    confirmation_code = ''.join(secrets.choice(code) for i in range(10))
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view([HTTPMethods.POST])
@permission_classes([AllowAny])
def get_jwt_token_for_user(request):
    """View function to get token for user."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if user.confirmation_code != confirmation_code:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
