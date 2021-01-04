from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Perfil, User
from ...dados_comuns.api.serializers import SecretariaSerializer, SetorSerializer
from ...dados_comuns.models import Setor


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer()
    nome = serializers.SerializerMethodField()
    secretaria = SecretariaSerializer()
    setor = SetorSerializer()

    def update(self, instance, validated_data):
        if 'setor' in validated_data:
            try:
                setor_ = Setor.objects.get(codigo=validated_data.get('setor').get('codigo'))
                instance.setor = setor_
            except ObjectDoesNotExist:
                raise ValidationError("Setor não existe")
        instance.save()
        return instance

    def get_nome(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ("username", "email", "perfil", "nome", "setor", "secretaria")
