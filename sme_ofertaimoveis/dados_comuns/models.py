import datetime
import uuid
from django.db import models


class Secretaria(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Secretaria"
        verbose_name_plural = "Secretarias"


class DiretoriaRegional(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)
    sigla = models.CharField("Sigla", max_length=2)
    codigo_eol = models.CharField("Código EOL", max_length=6)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
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
        verbose_name = "Subprefeitura"
        verbose_name_plural = "Subprefeituras"


class Distrito(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)
    subprefeitura = models.ForeignKey(Subprefeitura, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"


class Setor(models.Model):
    codigo = models.CharField("Código", max_length=4, null=True, blank=True)
    distrito = models.ForeignKey(Distrito, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.codigo}"

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"


class LogFluxoStatus(models.Model):
    (
        SOLICITACAO_REALIZADA,
        AGUARDANDO_ANALISE_PREVIA_SME,
        ENVIADO_COMAPRE,
        AGUARDANDO_RELATORIO_DE_VISTORIA,
        AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO,
        APROVADO,
        ENVIADO_DRE,
        FINALIZADO,
        CANCELADO,
    ) = range(9)

    STATUS_POSSIVEIS = (
        (SOLICITACAO_REALIZADA, 'Solicitação realizada'),
        (AGUARDANDO_ANALISE_PREVIA_SME, 'SME analisou previamente'),
        (ENVIADO_COMAPRE, 'Enviado à COMAPRE'),
        (AGUARDANDO_RELATORIO_DE_VISTORIA, 'Aguardando relatório de vistoria'),
        (AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO, 'Aguardando laudo de valor locatício'),
        (APROVADO, 'Aprovado'),
        (ENVIADO_DRE, 'Enviado à DRE'),
        (FINALIZADO, 'Finalizado'),
        (CANCELADO, 'Cancelado')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    criado_em = models.DateTimeField(
        'Criado em', editable=False, auto_now_add=True)
    descricao = models.TextField('Descricao', blank=True)
    justificativa = models.TextField('Justificativa', blank=True)
    status_evento = models.PositiveSmallIntegerField(choices=STATUS_POSSIVEIS)
    imovel = models.ForeignKey('imovel.Imovel', on_delete=models.CASCADE, blank=True, null=True, related_name='logs')
    usuario = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)

    @property
    def status_evento_explicacao(self):
        return self.get_status_evento_display()

    def __str__(self):
        data = datetime.strftime(self.criado_em, '%Y-%m-%d %H:%M:%S')
        return (f'{self.usuario} executou {self.get_status_evento_display()} '
                f'em {self.get_solicitacao_tipo_display()} no dia {data}')


class AnexoLog(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    log = models.ForeignKey(
        LogFluxoStatus,
        related_name='anexos',
        on_delete=models.DO_NOTHING
    )
    nome = models.CharField(max_length=255, blank=True)
    arquivo = models.FileField()

    def __str__(self):
        return f'Anexo {self.uuid} - {self.nome}'
