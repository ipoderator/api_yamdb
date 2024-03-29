from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserSignUpSerializer(serializers.Serializer):
    """Serializer for registration users."""

    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=([RegexValidator(regex=r"^[\w.@+-]+\Z")])
    )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Невозможно использовать username "me"!'
            )
        return data


class GetTokenSerializer(serializers.Serializer):
    """Serializer to get token."""

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=([RegexValidator(regex=r"^[\w.@+-]+\Z")])
    )
    confirmation_code = serializers.CharField(
        max_length=200,
        allow_blank=True,
        allow_null=True,
        required=True
    )

    def validate(self, data):
        if not data['confirmation_code']:
            raise serializers.ValidationError(
                'Неверный код подтверждения'
            )
        return data
