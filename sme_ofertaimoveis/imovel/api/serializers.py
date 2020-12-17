from rest_framework import serializers
from drf_base64.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from ..tasks import task_send_email_to_usuario, task_send_email_to_sme

from ..models import ContatoImovel, Imovel, Proponente, PlantaFoto
from ...dados_comuns.api.serializers import SetorSerializer


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

    def validate_arquivo(self, arquivo):
        filesize = arquivo.size

        if filesize > 15728640:
            raise ValidationError("O tamanho máximo de arquivos é 15MB")
        else:
            return arquivo

    class Meta:
        model = PlantaFoto
        exclude = ("id", "imovel")



class CadastroImovelSerializer(serializers.ModelSerializer):
    proponente = ProponenteSerializer()
    contato = ContatoSerializer()
    anexos = serializers.ListField(
        child=AnexoSerializer(), required=False
    )
    protocolo = serializers.SerializerMethodField()
    setor = SetorSerializer()

    def get_protocolo(self, obj):
        return obj.protocolo

    class Meta:
        model = Imovel
        fields = ["proponente", 
                  "anexos", 
                  "criado_em", 
                  "protocolo", 
                  "numero_iptu", 
                  "cep", 
                  "endereco", 
                  "numero", 
                  "complemento", 
                  "cidade", 
                  "uf",
                  "bairro", 
                  "complemento",
                  "contato", 
                  "observacoes",
                  "declaracao_responsabilidade",
                  "setor"]

    def create(self, validated_data):

        contato = ContatoSerializer().create(validated_data.pop("contato", {}))
        anexos = validated_data.pop('anexos', [])

        proponente = ProponenteSerializer().create(validated_data.pop("proponente", {}))

        imovel = Imovel.objects.filter(numero_iptu=validated_data.get("numero_iptu")).first()
        
        if imovel:
            raise ValidationError("Já existe um imovel com este IPTU cadastrado")
        else:
            imovel = Imovel.objects.create(proponente=proponente, contato=contato, **validated_data)

        tamanho_total_dos_arquivos = 0
        for anexo in anexos:
            filesize = anexo.get('arquivo').size
            tamanho_total_dos_arquivos += filesize
            if tamanho_total_dos_arquivos > 15728640:
                raise ValidationError("O tamanho total máximo dos arquivos é 15MB")
            PlantaFoto.objects.create(
                imovel=imovel, **anexo
            )
        # task_send_email_to_usuario.delay(proponente.email, imovel.protocolo)
        return imovel
