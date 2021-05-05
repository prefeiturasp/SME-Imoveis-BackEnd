from datetime import datetime
import uuid
from django.db import models


class Secretaria(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        ordering = ('nome',)
        verbose_name = "Secretaria"
        verbose_name_plural = "Secretarias"


class DiretoriaRegional(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)
    sigla = models.CharField("Sigla", max_length=2)
    codigo_eol = models.CharField("Código EOL", max_length=6)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        ordering = ('nome',)
        verbose_name = "DRE"
        verbose_name_plural = "DREs"


class Subprefeitura(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)
    dre = models.ManyToManyField(DiretoriaRegional,
                                 related_name='subprefeituras',
                                 blank=True)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        ordering = ('nome',)
        verbose_name = "Subprefeitura"
        verbose_name_plural = "Subprefeituras"


class Distrito(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)
    subprefeitura = models.ForeignKey(Subprefeitura, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        ordering = ('nome',)
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"


class Setor(models.Model):
    codigo = models.CharField("Código", max_length=4, null=True, blank=True)
    distrito = models.ForeignKey(Distrito, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.codigo}"

    class Meta:
        ordering = ('codigo',)
        verbose_name = "Setor"
        verbose_name_plural = "Setores"


class LogFluxoStatus(models.Model):
    (
        SOLICITACAO_REALIZADA,
        AGUARDANDO_ANALISE_PREVIA_SME,
        FINALIZADO_AREA_INSUFICIENTE,
        FINALIZADO_DEMANDA_INSUFICIENTE,
        FINALIZADO_NAO_ATENDE_NECESSIDADES,
        ENVIADO_COMAPRE,
        AGENDAMENTO_DA_VISTORIA,
        AGUARDANDO_RELATORIO_DE_VISTORIA,
        RELATORIO_VISTORIA,
        AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO,
        LAUDO_VALOR_LOCATICIO,
        VISTORIA_APROVADA,
        VISTORIA_REPROVADA,
        ENVIADO_DRE,
        FINALIZADO_APROVADO,
        FINALIZADO_REPROVADO,
        CANCELADO,
        REATIVADO
    ) = range(18)

    STATUS_POSSIVEIS = (
        (SOLICITACAO_REALIZADA, 'Solicitação Realizada'),
        (AGUARDANDO_ANALISE_PREVIA_SME, 'SME analisou previamente'),
        (FINALIZADO_AREA_INSUFICIENTE, 'Finalizado - Área Insuficiente'),
        (FINALIZADO_DEMANDA_INSUFICIENTE, 'Finalizado - Demanda Insuficiente'),
        (FINALIZADO_NAO_ATENDE_NECESSIDADES, 'Finalizado - Não atende as necessidades da SME'),
        (ENVIADO_COMAPRE, 'Enviado à COMAPRE'),
        (AGENDAMENTO_DA_VISTORIA, 'Agendamento da vistoria'),
        (AGUARDANDO_RELATORIO_DE_VISTORIA, 'Aguardando relatório de vistoria'),
        (RELATORIO_VISTORIA, 'Relatório da vistoria'),
        (AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO, 'Aguardando laudo de valor locatício'),
        (LAUDO_VALOR_LOCATICIO, 'Laudo de valor locatício'),
        (VISTORIA_APROVADA, 'Vistoria aprovada'),
        (VISTORIA_REPROVADA, 'Vistoria reprovada'),
        (ENVIADO_DRE, 'Enviado à DRE'),
        (FINALIZADO_APROVADO, 'Finalizado - Aprovado'),
        (FINALIZADO_REPROVADO, 'Finalizado - Reprovado'),
        (CANCELADO, 'Cancelado'),
        (REATIVADO, 'Reativado')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    criado_em = models.DateTimeField(
        'Criado em', editable=False, auto_now_add=True)
    descricao = models.TextField('Descricao', blank=True)
    justificativa = models.TextField('Justificativa', blank=True)
    status_evento = models.PositiveSmallIntegerField(choices=STATUS_POSSIVEIS)
    email_enviado = models.BooleanField('Email enviado', blank=True, null=True)
    data_agendada = models.DateTimeField('Data agendada', blank=True, null=True)
    imovel = models.ForeignKey('imovel.Imovel', on_delete=models.CASCADE, blank=True, null=True, related_name='logs')
    usuario = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)
    processo_sei = models.TextField('Numero processo SEI', blank=True, null=True)
    nome_da_unidade = models.TextField('Nome da unidade', blank=True, null=True)

    @property
    def status_evento_explicacao(self):
        return self.get_status_evento_display()

    def __str__(self):
        data = datetime.strftime(self.criado_em, '%Y-%m-%d %H:%M:%S')
        return (f'{self.usuario.first_name} {self.usuario.last_name} executou {self.get_status_evento_display()} no dia {data}')

    class Meta:
        ordering = ('id',)

class AnexoLog(models.Model):
    TIPO_DOCUMENTO = (
        (0, 'Relatório de vistoria'),
        (1, 'Relatório fotográfico'),
        (2, 'Planta atual'),
        (3, 'Planta com adequações'),
        (4, 'Plano de adequação'),
        (5, 'Laudo de valor locatício'),
    )

    TIPO_ARQUIVO = (
        (0, 'Imagem'),
        (1, 'Documento')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    log = models.ForeignKey(
        LogFluxoStatus,
        related_name='anexos',
        on_delete=models.DO_NOTHING
    )
    nome = models.CharField(max_length=255, blank=True)
    arquivo = models.FileField()
    tipo_documento = models.SmallIntegerField(
        'Tipo Documento', choices=TIPO_DOCUMENTO, default=4
    )
    tipo_arquivo = models.SmallIntegerField(
        'Tipo Arquivo', choices=TIPO_ARQUIVO, blank=True, null=True
    )

    def as_dict(self):
        return {
            "log": self.log.id,
            "arquivo": self.arquivo,
            "tipo_documento": self.tipo_documento,
            "uuid": self.uuid
        }

    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
