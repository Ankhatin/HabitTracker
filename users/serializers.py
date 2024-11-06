from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для работы с данными модели пользователь (User)
    """

    class Meta:
        model = User
        fields = ["email", "phone", "password", "tg_username", "tg_id"]


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token
