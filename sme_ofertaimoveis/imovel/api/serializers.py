from rest_framework import serializers
from drf_base64.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from ..models import (
    ContatoImovel, Imovel, Proponente, PlantaFoto, TipoProponente
)


class TipoProponenteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoProponente
        fields = ['pk_tipo_proponente', 'nome']


class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoImovel
        exclude = ("id",)


class ProponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proponente
        exclude = ("id",)


class PlantaFotoSerializer(ModelSerializer):

    def validate_planta(self, planta):
        filesize = planta.size

        if filesize > 10485760:
            raise ValidationError("O tamanho máximo de um arquivo é 10MB")
        else:
            return planta

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
    proponente = ProponenteSerializer(required=False)
    contato = ContatoSerializer()
    endereco = EnderecoSerializer()
    planta_fotos = serializers.ListField(
        child=PlantaFotoSerializer()
    )
    protocolo = serializers.SerializerMethodField()

    def get_protocolo(self, obj):
        return obj.protocolo

    class Meta:
        model = Imovel
        fields = ["proponente", "contato", "endereco", "planta_fotos", "criado_em", "protocolo"]

    def create(self, validated_data):
        contato = ContatoSerializer().create(validated_data.pop("contato", {}))
        proponente = None
        if 'proponente' in validated_data:
            proponente = ProponenteSerializer().create(validated_data.pop("proponente", {}))

        endereco = validated_data.pop("endereco")
        validated_data.update(endereco)

        planta_fotos = validated_data.pop('planta_fotos', [])
        imovel = Imovel.objects.create(
            contato=contato, proponente=proponente, **validated_data
        )

        tamanho_total_dos_arquivos = 0
        for planta_foto in planta_fotos:
            filesize = planta_foto.get('planta').size
            tamanho_total_dos_arquivos += filesize
            if tamanho_total_dos_arquivos > 10485760:
                raise ValidationError("O tamanho total máximo dos arquivos é 10MB")
            PlantaFoto.objects.create(
                imovel=imovel, planta=planta_foto.get("planta")
            )

        return imovel
