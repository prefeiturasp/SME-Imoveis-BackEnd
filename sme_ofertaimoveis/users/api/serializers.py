from rest_framework import serializers

from ..models import Perfil, User


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer()
    nome = serializers.SerializerMethodField()

    def get_nome(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ("username", "email", "perfil", "nome")
