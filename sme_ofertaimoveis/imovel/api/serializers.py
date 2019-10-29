from rest_framework import serializers
from drf_base64.serializers import ModelSerializer

from ..models import ContatoImovel, Imovel, Proponente, PlantaFoto


class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoImovel
        exclude = ("id",)


class ProponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proponente
        exclude = ("id",)


class PlantaFotoSerializer(ModelSerializer):
    
    class Meta:
        model = PlantaFoto
        exclude = ("id", "imovel") 
        

class EnderecoSerializer(serializers.ModelSerializer):
    def get_attribute(self, obj):
        return obj

    class Meta:
        model = Imovel
        exclude = ("id", "proponente", "contato")


class ImovelSerializer(serializers.ModelSerializer):

    proponente = ProponenteSerializer()
    contato = ContatoSerializer()
    endereco = EnderecoSerializer()
    planta_fotos = serializers.ListField(
        child=PlantaFotoSerializer()
    )

    class Meta:
        model = Imovel
        fields = ["proponente", "contato", "endereco", "planta_fotos", "criado_em"]

    def create(self, validated_data):
        contato = ContatoSerializer().create(validated_data.pop("contato", {}))
        proponente = ProponenteSerializer().create(validated_data.pop("proponente", {}))
        
        endereco = validated_data.pop("endereco")
        validated_data.update(endereco)

        planta_fotos = validated_data.pop('planta_fotos', [])
        imovel = Imovel.objects.create(
            contato=contato, proponente=proponente, **validated_data
        )

        for planta_foto in planta_fotos:
            PlantaFoto.objects.create(
                imovel=imovel, planta=planta_foto.get("planta")
            )

        return imovel
