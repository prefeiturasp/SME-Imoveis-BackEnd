from rest_framework import serializers

from ..models import ContatoImovel, Imovel, Proponente


class ContatoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContatoImovel
        exclude = ('id',)


class ProponenteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proponente
        exclude = ('id',)


class ImovelSerializer(serializers.ModelSerializer):

    proponente = ProponenteSerializer()
    contato = ContatoSerializer()

    class Meta:
        model = Imovel
        exclude = ('id',"planta")

    def create(self, validated_data):
        contato = ContatoSerializer().create(
            validated_data.pop('contato', {})
        )
        proponente = ProponenteSerializer().create(
            validated_data.pop('proponente', {})
        )

        return Imovel.objects.create(
            contato=contato, 
            proponente=proponente, 
            **validated_data
        )