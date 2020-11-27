from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    perfil_usuario = serializers.CharField(required=False)

    def create(self, validated_data):  # noqa C901
        pass

    class Meta:
        model = User
        fields = ("username", "email",)
