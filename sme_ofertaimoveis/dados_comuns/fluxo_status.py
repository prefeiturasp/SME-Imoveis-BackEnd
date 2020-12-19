import xworkflows

from django.db import models
from django_xworkflows import models as xwf_models

from sme_ofertaimoveis.dados_comuns.models import LogFluxoStatus


class ImoveisWorkflow(xwf_models.Workflow):
    log_model = ''

    AGUARDANDO_ANALISE_PREVIA_SME = 'AGUARDANDO_ANALISE_PREVISA_SME'
    ENVIADO_COMAPRE = 'ENVIADO_COMAPRE'
    AGUARDANDO_RELATORIO_DE_VISTORIA = 'AGUARDANDO_RELATORIO_DE_VISTORIA'
    AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO = 'AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO'
    APROVADO = 'APROVADO'
    ENVIADO_DRE = 'ENVIADO_DRE'
    FINALIZADO = 'FINALIZADO'
    CANCELADO = 'CANCELADO'

    states = (
        (AGUARDANDO_ANALISE_PREVIA_SME, 'Aguardando análise prévia da SME'),
        (ENVIADO_COMAPRE, 'Enviado à COMPAPRE'),
        (AGUARDANDO_RELATORIO_DE_VISTORIA, 'Aguardando relatório de vistoria'),
        (AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO, 'Aguardando laudo de valor locatício'),
        (APROVADO, 'Aprovado'),
        (ENVIADO_DRE, 'Enviado à DRE'),
        (FINALIZADO, 'Finalizado'),
        (CANCELADO, 'Cancelado')
    )

    transitions = (
        ('envia_a_comapre', AGUARDANDO_ANALISE_PREVIA_SME, ENVIADO_COMAPRE),
        ('aguarda_relatorio_vistoria', ENVIADO_COMAPRE, AGUARDANDO_RELATORIO_DE_VISTORIA),
        ('aguarda_laudo_valor_locaticio', AGUARDANDO_RELATORIO_DE_VISTORIA, AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO),
        ('aprova', AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO, APROVADO),
        ('envia_a_dre', APROVADO, ENVIADO_DRE),
        ('finaliza', ENVIADO_DRE, FINALIZADO),
        ('cancela', [AGUARDANDO_ANALISE_PREVIA_SME, ENVIADO_COMAPRE, AGUARDANDO_RELATORIO_DE_VISTORIA,
                     AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO, APROVADO, ENVIADO_DRE, FINALIZADO, CANCELADO],
         CANCELADO)
    )

    initial_state = AGUARDANDO_ANALISE_PREVIA_SME


class FluxoImoveis(xwf_models.WorkflowEnabled, models.Model):
    workflow_class = ImoveisWorkflow
    status = xwf_models.StateField(workflow_class)

    def salvar_log_transicao(self, status_evento, usuario, **kwargs):
        raise NotImplementedError('Deve criar um método salvar_log_transicao')

    @xworkflows.after_transition('')
    def _envia_a_comapre_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.ENVIADO_COMAPRE,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''))

    class Meta:
        abstract = True
