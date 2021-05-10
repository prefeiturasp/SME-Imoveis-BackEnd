import uuid
from datetime import datetime
import environ

from django.db import models
from django.core import validators

from .validators import phone_validation, cep_validation, cpf_cnpj_validation
from .managers import SME_ContatosManager
from .utils import get_width
from ..dados_comuns.fluxo_status import FluxoImoveis
from ..dados_comuns.models import Secretaria, Setor, LogFluxoStatus

env = environ.Env()

class SME_Contatos(models.Model):
    nome = models.CharField("Nome", max_length=255)
    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()]
    )
    ativo = models.BooleanField("Esta ativo", default=True)
    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    objects = SME_ContatosManager()

    def __str__(self):
        return f"{self.nome} => {self.email}"

    class Meta:
        verbose_name = "Contato Prefeitura"
        verbose_name_plural = "Contatos Prefeitura"


class Proponente(models.Model):
    IMOBILIARIA = 1
    PROCURADOR = 2
    ONG = 3
    OUTRO = 4

    TYPES = (
        (0, "----SELECIONE-----"),
        (IMOBILIARIA, "Imobiliária"),
        (PROCURADOR, "Procurador"),
        (ONG, "Ong"),
        (OUTRO, "Outro"),
    )

    TIPO_PROPONENTE = (
        (0, "Não Informado"),
        (1, "Proprietário"),
        (2, "Representante Legal")
    )

    tipo = models.PositiveSmallIntegerField("Tipo", choices=TYPES, default=OUTRO)

    tipo_proponente = models.PositiveSmallIntegerField("Tipo de Proponente", choices=TIPO_PROPONENTE, default=0)

    nome = models.CharField("Nome", max_length=255, blank=True, null=True)
    cpf_cnpj = models.CharField(
        "CPF / CNPJ", max_length=20, validators=[cpf_cnpj_validation]
        , blank=True, null=True, default=""
    )
    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()]
        , blank=True, null=True, default=""
    )
    telefone = models.CharField(
        "Telefone", max_length=20, validators=[phone_validation]
        , blank=True, null=True, default=""
    )
    # Added in 11/26/2020 new feature/27865-28434
    celular = models.CharField(
        verbose_name="Celular",
        max_length=20,
        validators=[phone_validation],
        blank=True,
        null=True,
        default=""
    )
    situacao = models.CharField(
        verbose_name="Status", max_length=255, blank=True, null=True, default=""
    )
    # end feature
    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    def __str__(self):
        phone = ""
        if self.celular:
            phone = self.celular
        elif self.telefone:
            phone = self.telefone
        return f"{self.nome} => {self.email} " f"{phone}"

    class Meta:
        verbose_name = "Proponente"
        verbose_name_plural = "Proponentes"


class ContatoImovel(models.Model):
    nome = models.CharField("Nome", max_length=255)
    cpf_cnpj = models.CharField("CPF / CNPJ", max_length=20)
    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()]
        , blank=True, null=True, default=""
    )
    telefone = models.CharField(
        "Telefone", max_length=20, validators=[phone_validation]
        , blank=True, null=True, default=""
    )
    # Added in 11/26/2020 new feature/27865-28434
    celular = models.CharField(
        verbose_name="Celular",
        max_length=20,
        validators=[phone_validation],
        default="(11) 9 9111-1111"
    )
    # Ended feature/27865-28434
    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    def __str__(self):
        return f"{self.nome} => {self.cpf_cnpj}"

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"


class Imovel(FluxoImoveis):
    UFChoices = (
        ('AC', 'Acre'),
        ('AL', "Alagoas"),
        ('AP', "Amapá"),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    )

    proponente = models.ForeignKey(Proponente, on_delete=models.DO_NOTHING, blank=True, null=True)
    contato = models.ForeignKey(ContatoImovel, on_delete=models.DO_NOTHING, null=True)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.SET_NULL, null=True)

    cep = models.CharField("CEP", max_length=20, validators=[cep_validation])
    endereco = models.CharField("Logradouro", max_length=255)
    cidade = models.CharField("Cidade", max_length=255, null=True, blank=True)
    uf = models.CharField("UF", max_length=2, choices=UFChoices, null=True, blank=True)
    bairro = models.CharField("Bairro", max_length=255)
    numero = models.CharField("Numero", max_length=255)
    complemento = models.CharField("Complemento", max_length=255, null=True, blank=True)

    latitude = models.CharField("Latitude", max_length=255)
    longitude = models.CharField("longitude", max_length=255)
    numero_iptu = models.CharField("Numero IPTU", max_length=20, blank=True, default="")
    nao_possui_iptu = models.BooleanField(default=False)
    # Added in 11/26/2020 new feature/27865-28434
    area_construida = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    situacao = models.CharField(
        verbose_name="Situação", max_length=255, null=False, blank=False, default="Novo"
    )
    declaracao_responsabilidade = models.BooleanField(default=True)
    # end feature
    observacoes = models.TextField(blank=True, null=True)

    codigo_eol = models.CharField("Codigo EOL", max_length=255, null=True, blank=True)
    escola = models.CharField("Escola", max_length=255, null=True, blank=True)

    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    # Valores String vazia, Registro com duplicidade de IPTU, Registro com duplicidade de Endereço 
    situacao_duplicidade = models.CharField("Situação Duplicidade", max_length=255, null=True, blank=True, default='')
    excluido = models.BooleanField(default=False)


    @property
    def anexos(self):
        return self.plantafoto_set.all()

    @property
    def protocolo(self):
        if self.id:
            return "{:03d}".format(self.id)
        return ""

    def __str__(self):
        return f"{self.contato} => {self.endereco}"

    def salvar_log_transicao(self, status_evento, usuario, **kwargs):
        justificativa = kwargs.get('justificativa', '')
        email_enviado = kwargs.get('email_enviado', False)
        data_agendada = kwargs.get('data_agendada', None)
        processo_sei = kwargs.get('processo_sei', None)
        nome_da_unidade = kwargs.get('nome_da_unidade', None)
        LogFluxoStatus.objects.create(
            descricao=str(self),
            status_evento=status_evento,
            usuario=usuario,
            imovel=self,
            justificativa=justificativa,
            email_enviado=email_enviado,
            data_agendada=data_agendada,
            processo_sei=processo_sei,
            nome_da_unidade=nome_da_unidade
        )
    
    

    def as_dict(self):
        from .relatorio.constants import FLUXO

        log_vistoria = self.logs.filter(status_evento=6).first()
        data_vistoria = datetime.strftime(log_vistoria.data_agendada, "%d/%m/%Y") if log_vistoria else ''
        log_cancelamento = self.logs.filter(status_evento=16).first()
        data_cancelamento = datetime.strftime(log_cancelamento.data_agendada, "%d/%m/%Y") if log_cancelamento else ''
        data_atualizacao_demanda = datetime.strftime(self.demandaimovel.data_atualizacao, "%d/%m/%Y") if self.demandaimovel.data_atualizacao else ''
        diretoria_regional_educacao = self.setor.distrito.subprefeitura.dre.first().nome.capitalize()

        def logs_as_dict(logs):
            _logs = []
            for log in logs:
                _logs.append({
                    'criado_em': datetime.strftime(log.criado_em, "%d/%m/%Y"),
                    'status_evento_explicacao': log.status_evento_explicacao,
                    'usuario': {
                        'nome': log.usuario.get_full_name(),
                        'username': log.usuario.username,
                    }
                })
            return _logs

        return {
            'react_url': env('REACT_APP_URL'),
            'uuid': self.id,
            'protocolo': self.protocolo,
            'proponente_cpf_cnpj': self.proponente.cpf_cnpj,
            'proponente_nome': self.proponente.nome,
            'proponente_email': self.proponente.email,
            'proponente_telefone': self.proponente.telefone,
            'proponente_celular': self.proponente.celular,
            'proponente_tipo': self.proponente.get_tipo_proponente_display(),
            'area_construida': self.area_construida,
            'endereco': self.endereco,
            'complemento': self.complemento,
            'numero': self.numero,
            'bairro': self.bairro,
            'cep': self.cep,
            'cidade': self.cidade,
            'criado_em': datetime.strftime(self.criado_em, "%d/%m/%Y"),
            'uf': self.uf,
            'numero_iptu': self.numero_iptu,
            'observacoes': self.observacoes,
            'diretoria_regional_educacao': diretoria_regional_educacao,
            'distrito': self.setor.distrito.nome.capitalize(),
            'codigo_setor': self.setor.codigo,
            'data_vistoria': data_vistoria,
            'data_cancelamento': data_cancelamento,
            'data_hoje': datetime.strftime(datetime.now(), "%d/%m/%Y"),
            'bercario_i': self.demandaimovel.bercario_i,
            'bercario_ii': self.demandaimovel.bercario_ii,
            'mini_grupo_i': self.demandaimovel.mini_grupo_i,
            'mini_grupo_ii': self.demandaimovel.mini_grupo_ii,
            'demanda_total': self.demandaimovel.total,
            'fluxo': FLUXO,
            'data_atualizacao_demanda': data_atualizacao_demanda,
            'width': get_width(FLUXO, self.logs.all()),
            'logs': logs_as_dict(self.logs.all()),
            'nao_possui_iptu': self.nao_possui_iptu,
        }

    class Meta:
        verbose_name = "Imovel"
        verbose_name_plural = "Imoveis"
        ordering = ('id',)


class PlantaFoto(models.Model):
    TIPO_DOCUMENTO = (
        (0, 'Fotos da Fachada'),
        (1, 'Fotos do Ambiente Interno'),
        (2, 'Fotos de Área Externa'),
        (3, 'Cópia do IPTU ou ITR'),
        (4, 'Cópia da Planta ou Croqui'),
    )

    TIPO_ARQUIVO = (
        (0, 'Imagem'),
        (1, 'Documento')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    arquivo = models.FileField()
    # Added in 11/26/2020 new feature/27865-28434
    tipo_documento = models.SmallIntegerField(
        'Tipo Documento', choices=TIPO_DOCUMENTO, default=4
    )
    tipo_arquivo = models.SmallIntegerField(
        'Tipo Arquivo', choices=TIPO_ARQUIVO, blank=True, null=True
    )
    # End feature/27865-28434
    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    def as_dict(self):
        return {
            "imovel": self.imovel.id,
            "arquivo": self.arquivo,
            "tipo_documento": self.tipo_documento,
            "uuid": self.uuid
        }

    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"


class DemandaImovel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imovel = models.OneToOneField(Imovel, on_delete=models.CASCADE)
    bercario_i = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    bercario_ii = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    mini_grupo_i = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    mini_grupo_ii = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    data_atualizacao = models.DateTimeField("Data Atualização", blank=True, null=True)

    @property
    def total(self):
        return self.bercario_i + self.bercario_ii + self.mini_grupo_i + self.mini_grupo_ii

    def __str__(self):
        return f"{self.imovel.endereco} => total demanda: {self.total}"

    class Meta:
        verbose_name = "Demanda"
        verbose_name_plural = "Demandas"
