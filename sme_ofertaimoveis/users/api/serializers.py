from rest_framework import serializers

from ..models import Perfil, User
from ...dados_comuns.api.serializers import SecretariaSerializer


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer()
    nome = serializers.SerializerMethodField()
    secretaria = SecretariaSerializer()
    setor = serializers.SerializerMethodField()

    def get_nome(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def get_setor(self, obj):
        if obj.setor:
            return {'codigo': obj.setor.codigo, 'dre': obj.setor.distrito.subprefeitura.dre.first().sigla}
        return None

    class Meta:
        model = User
        fields = ("username", "email", "perfil", "nome", "setor", "secretaria")
