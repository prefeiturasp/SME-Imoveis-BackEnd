import requests
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from django.conf import settings
from drf_base64.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from ..tasks import task_send_email_to_usuario, task_send_email_to_sme

from ..models import ContatoImovel, Imovel, Proponente, PlantaFoto, DemandaImovel
from ...dados_comuns.api.serializers import SetorSerializer
from ...dados_comuns.api.serializers.log_fluxo_status_serializer import LogFluxoStatusSerializer
from ...dados_comuns.models import Setor


class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoImovel
        exclude = ("id",)

    def create(self, validated_data):
        cpf_cnpj = validated_data.get("cpf_cnpj")
        contato = ContatoImovel.objects.filter(cpf_cnpj=cpf_cnpj).first()

        if contato:
            contato.nome = validated_data.get("nome")
            contato.telefone = validated_data.get("telefone")
            contato.email = validated_data.get("email")
            contato.celular = validated_data.get("celular")
        else:
            contato = ContatoImovel.objects.create(**validated_data)
        return contato


class ProponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proponente
        exclude = ("id",)

    def create(self, validated_data):
        cpf_cnpj = validated_data.get("cpf_cnpj")
        proponente = Proponente.objects.filter(cpf_cnpj=cpf_cnpj).first()

        if proponente:
            proponente.nome = validated_data.get("nome")
            proponente.email = validated_data.get("email")
            proponente.telefone = validated_data.get("telefone", None)
            proponente.celular = validated_data.get("celular")
            proponente.tipo_proponente = validated_data.get("tipo_proponente")
            proponente.save()
        else:
            proponente = Proponente.objects.create(**validated_data)
        return proponente


class AnexoSerializer(ModelSerializer):
    get_tipo_documento_display = serializers.CharField(required=False)

    def validate_arquivo(self, arquivo):
        filesize = arquivo.size

        if filesize > 15728640:
            raise ValidationError("O tamanho máximo de arquivos é 15MB")
        else:
            return arquivo

    class Meta:
        model = PlantaFoto
        exclude = ("id", "imovel")


class AnexoCreateSerializer(serializers.ModelSerializer):
    imovel = serializers.IntegerField()
    tipo_documento = serializers.IntegerField()

    def create(self, validated_data):
        imovel_id = validated_data.pop('imovel')
        imovel = Imovel.objects.get(id=imovel_id)
        anexo = PlantaFoto.objects.create(
            imovel=imovel,
            **validated_data)
        return anexo.as_dict()

    class Meta:
        model = PlantaFoto
        exclude = ('id',)


class DemandaImovelSerializer(ModelSerializer):
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.total

    class Meta:
        model = DemandaImovel
        exclude = ('uuid', 'imovel',)


class CadastroImovelSerializer(serializers.ModelSerializer):
    proponente = ProponenteSerializer()
    contato = ContatoSerializer()
    anexos = serializers.ListField(
        child=AnexoSerializer(), required=False
    )
    protocolo = serializers.SerializerMethodField()
    setor = SetorSerializer(required=False)
    logs = LogFluxoStatusSerializer(many=True, required=False)
    demandaimovel = DemandaImovelSerializer(required=False)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()

    def get_protocolo(self, obj):
        return obj.protocolo

    class Meta:
        model = Imovel
        fields = [
            "id",
            "proponente",
            "anexos",
            "area_construida",
            "criado_em",
            "protocolo",
            "numero_iptu",
            "cep",
            "endereco",
            "latitude",
            "longitude",
            "numero",
            "complemento",
            "cidade",
            "uf",
            "bairro",
            "complemento",
            "contato",
            "observacoes",
            "declaracao_responsabilidade",
            "status",
            "setor",
            "logs",
            "demandaimovel",
            "nao_possui_iptu"]

    def create(self, validated_data):
        contato = ContatoSerializer().create(validated_data.pop("contato", {}))
        anexos = validated_data.pop('anexos', [])

        proponente = ProponenteSerializer().create(validated_data.pop("proponente", {}))

        imovel = Imovel.objects.filter(numero_iptu=validated_data.get("numero_iptu")).first()

        if imovel:
            raise ValidationError("Já existe um imovel com este IPTU cadastrado")
        else:
            imovel = Imovel.objects.create(proponente=proponente, contato=contato, **validated_data)

        url = f'{settings.SCIEDU_URL}/{imovel.latitude}/{imovel.longitude}'
        headers = {
            "Authorization": f'Token {settings.SCIEDU_TOKEN}',
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        results = response.json().get('results')
        bercario_i = next(item for item in results if item["cd_serie_ensino"] == 1)
        demanda_imovel = DemandaImovel(imovel=imovel)
        if bercario_i:
            demanda_imovel.bercario_i = bercario_i.get('total')
        bercario_ii = next(item for item in results if item["cd_serie_ensino"] == 4)
        if bercario_ii:
            demanda_imovel.bercario_ii = bercario_ii.get('total')
        mini_grupo_i = next(item for item in results if item["cd_serie_ensino"] == 27)
        if mini_grupo_i:
            demanda_imovel.mini_grupo_i = mini_grupo_i.get('total')
        mini_grupo_ii = next(item for item in results if item["cd_serie_ensino"] == 28)
        if mini_grupo_ii:
            demanda_imovel.mini_grupo_ii = mini_grupo_ii.get('total')
        demanda_imovel.save()

        tamanho_total_dos_arquivos = 0
        for anexo in anexos:
            filesize = anexo.get('arquivo').size
            tamanho_total_dos_arquivos += filesize
            if tamanho_total_dos_arquivos > 15728640:
                raise ValidationError("O tamanho total máximo dos arquivos é 15MB")
            PlantaFoto.objects.create(
                imovel=imovel, **anexo
            )
        task_send_email_to_usuario.delay(proponente.email, imovel.protocolo)
        return imovel

    def update(self, instance, validated_data):
        validated_data.pop('anexos', [])
        setor = validated_data.pop('setor', None)
        if setor.get('codigo'):
            setor = Setor.objects.get(codigo=setor.get('codigo'))
        else:
            setor = None
        validated_data.pop('demandaimovel', [])
        if 'logs' in validated_data:
            validated_data.pop('logs')
        contato = ContatoSerializer().create(validated_data.pop("contato", {}))
        proponente = ProponenteSerializer().create(validated_data.pop("proponente", {}))

        Imovel.objects.filter(
            id=instance.id).update(
            setor=setor, proponente=proponente, contato=contato, **validated_data)
        imovel = Imovel.objects.get(id=instance.id)

        url = f'{settings.SCIEDU_URL}/{imovel.latitude}/{imovel.longitude}'
        headers = {
            "Authorization": f'Token {settings.SCIEDU_TOKEN}',
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        results = response.json().get('results')
        print(results)
        DemandaImovel.objects.filter(imovel=imovel).delete()
        bercario_i = next(item for item in results if item["cd_serie_ensino"] == 1)
        demanda_imovel = DemandaImovel(imovel=imovel)
        if bercario_i:
            demanda_imovel.bercario_i = bercario_i.get('total')
        bercario_ii = next(item for item in results if item["cd_serie_ensino"] == 4)
        if bercario_ii:
            demanda_imovel.bercario_ii = bercario_ii.get('total')
        mini_grupo_i = next(item for item in results if item["cd_serie_ensino"] == 27)
        if mini_grupo_i:
            demanda_imovel.mini_grupo_i = mini_grupo_i.get('total')
        mini_grupo_ii = next(item for item in results if item["cd_serie_ensino"] == 28)
        if mini_grupo_ii:
            demanda_imovel.mini_grupo_ii = mini_grupo_ii.get('total')
        demanda_imovel.save()

        return imovel
