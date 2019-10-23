from rest_framework import serializers

from ..models import ContatoImovel, Imovel, Proponente


class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoImovel
        exclude = ("id",)


class ProponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proponente
        exclude = ("id",)


class EnderecoSerializer(serializers.ModelSerializer):
    def get_attribute(self, obj):
        return obj

    class Meta:
        model = Imovel
        exclude = ("id", "proponente", "contato", "planta")


class ImovelSerializer(serializers.ModelSerializer):

    proponente = ProponenteSerializer()
    contato = ContatoSerializer()
    endereco = EnderecoSerializer()

    class Meta:
        model = Imovel
        fields = ["proponente", "contato", "endereco", "criado_em"]

    def create(self, validated_data):
        contato = ContatoSerializer().create(validated_data.pop("contato", {}))
        proponente = ProponenteSerializer().create(validated_data.pop("proponente", {}))
        endereco = validated_data.pop("endereco")
        validated_data.update(endereco)

        return Imovel.objects.create(
            contato=contato, proponente=proponente, **validated_data
        )
