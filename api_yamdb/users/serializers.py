from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

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


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        unique=True,
        required=True
    )
    username = serializers.CharField(
        max_length=150,
        unique=True,
        required=True,
        validators=([RegexValidator(regex=r"^[\w.@+-]+\Z")])
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Невозможно использовать username "me"!'
            )
        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        unique=True,
        required=True,
        validators=([RegexValidator(regex=r"^[\w.@+-]+\Z")])
    )
    confirmation_code = serializers.CharField(
        max_length=200,
        blank=True,
        null=True,
        unique=True,
        required=True
    )

    class Meta:
        model = User
        fields = ('confirmation_code', 'username')

    def validate(self, data):
        if not data['confirmation_code']:
            raise serializers.ValidationError(
                'Неверный код подтверждения'
            )
        return data
