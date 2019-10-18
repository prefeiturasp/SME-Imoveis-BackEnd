from rest_framework import serializers

from ..models import Contato, Imovel


class ContatoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contato
        exclude = ('id',)


class ImovelSerializer(serializers.ModelSerializer):
    contato = ContatoSerializer()

    class Meta:
        model = Imovel
        exclude = ('id',"planta")

    def create(self, validated_data):
        contato = ContatoSerializer().create(
            validated_data.pop('contato', {})
        )

        return Imovel.objects.create(contato=contato, **validated_data)