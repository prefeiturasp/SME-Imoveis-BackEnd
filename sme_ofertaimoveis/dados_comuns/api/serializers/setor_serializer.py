from rest_framework import serializers

from . import DreSerializer
from ...models import Setor


class SetorSerializer(serializers.ModelSerializer):
    dre = serializers.SerializerMethodField()

    def get_dre(self, obj):
        return DreSerializer(obj.distrito.subprefeitura.dre.first()).data

    class Meta:
        model = Setor
        fields = '__all__'
