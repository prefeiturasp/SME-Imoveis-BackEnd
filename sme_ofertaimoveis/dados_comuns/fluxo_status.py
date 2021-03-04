import xworkflows

from django.db import models
from django_xworkflows import models as xwf_models

from sme_ofertaimoveis.dados_comuns.models import LogFluxoStatus


class ImoveisWorkflow(xwf_models.Workflow):
    log_model = ''

    SOLICITACAO_REALIZADA = 'SOLICITACAO_REALIZADA'
    AGUARDANDO_ANALISE_PREVIA_SME = 'AGUARDANDO_ANALISE_PREVIA_SME'
    FINALIZADO_AREA_INSUFICIENTE = 'FINALIZADO_AREA_INSUFICIENTE'
    FINALIZADO_DEMANDA_INSUFICIENTE = 'FINALIZADO_DEMANDA_INSUFICIENTE'
    FINALIZADO_NAO_ATENDE_NECESSIDADES = 'FINALIZADO_NAO_ATENDE_NECESSIDADES'
    ENVIADO_COMAPRE = 'ENVIADO_COMAPRE'
    AGENDAMENTO_DA_VISTORIA = 'AGENDAMENTO_DA_VISTORIA'
    AGUARDANDO_RELATORIO_DE_VISTORIA = 'AGUARDANDO_RELATORIO_DE_VISTORIA'
    RELATORIO_VISTORIA = 'RELATORIO_VISTORIA'
    AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO = 'AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO'
    LAUDO_VALOR_LOCATICIO = 'LAUDO_VALOR_LOCATICIO'
    VISTORIA_APROVADA = 'VISTORIA_APROVADA'
    VISTORIA_REPROVADA = 'VISTORIA_REPROVADA'
    ENVIADO_DRE = 'ENVIADO_DRE'
    FINALIZADO_APROVADO = 'FINALIZADO_APROVADO'
    FINALIZADO_REPROVADO = 'FINALIZADO_REPROVADO'
    CANCELADO = 'CANCELADO'
    REATIVADO = 'REATIVADO'

    states = (
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

    transitions = (
        ('sme_analisa_previamente', SOLICITACAO_REALIZADA, AGUARDANDO_ANALISE_PREVIA_SME),
        ('finaliza_area_insuficiente', AGUARDANDO_ANALISE_PREVIA_SME, FINALIZADO_AREA_INSUFICIENTE),
        ('finaliza_demanda_insuficiente', AGUARDANDO_ANALISE_PREVIA_SME, FINALIZADO_DEMANDA_INSUFICIENTE),
        ('finaliza_nao_atende_necessidades', AGUARDANDO_ANALISE_PREVIA_SME, FINALIZADO_NAO_ATENDE_NECESSIDADES),
        ('envia_a_comapre', AGUARDANDO_ANALISE_PREVIA_SME, ENVIADO_COMAPRE),
        ('agenda_vistoria', ENVIADO_COMAPRE, AGENDAMENTO_DA_VISTORIA),
        ('aguarda_relatorio_vistoria', AGENDAMENTO_DA_VISTORIA, AGUARDANDO_RELATORIO_DE_VISTORIA),
        ('relatorio_vistoria', AGUARDANDO_RELATORIO_DE_VISTORIA, RELATORIO_VISTORIA),
        ('aguarda_laudo_valor_locaticio', RELATORIO_VISTORIA, AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO),
        ('laudo_valor_locaticio', AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO, LAUDO_VALOR_LOCATICIO),
        ('aprova_vistoria', LAUDO_VALOR_LOCATICIO, VISTORIA_APROVADA),
        ('reprova_vistoria', LAUDO_VALOR_LOCATICIO, VISTORIA_REPROVADA),
        ('envia_a_dre', VISTORIA_APROVADA, ENVIADO_DRE),
        ('finaliza_aprovado', ENVIADO_DRE, FINALIZADO_APROVADO),
        ('finaliza_reprovado', VISTORIA_REPROVADA, FINALIZADO_REPROVADO),
        ('cancela', [ SOLICITACAO_REALIZADA, AGUARDANDO_ANALISE_PREVIA_SME, FINALIZADO_AREA_INSUFICIENTE,
                        FINALIZADO_DEMANDA_INSUFICIENTE, FINALIZADO_NAO_ATENDE_NECESSIDADES, ENVIADO_COMAPRE,
                        AGENDAMENTO_DA_VISTORIA, AGUARDANDO_RELATORIO_DE_VISTORIA, RELATORIO_VISTORIA,
                        AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO, LAUDO_VALOR_LOCATICIO, VISTORIA_APROVADA,
                        VISTORIA_REPROVADA, ENVIADO_DRE, FINALIZADO_APROVADO,
                        FINALIZADO_REPROVADO, REATIVADO ], CANCELADO),
        ('reativa', [ CANCELADO, FINALIZADO_AREA_INSUFICIENTE, FINALIZADO_DEMANDA_INSUFICIENTE,
                        FINALIZADO_NAO_ATENDE_NECESSIDADES, FINALIZADO_REPROVADO ], REATIVADO)
    )

    initial_state = SOLICITACAO_REALIZADA


class FluxoImoveis(xwf_models.WorkflowEnabled, models.Model):
    workflow_class = ImoveisWorkflow
    status = xwf_models.StateField(workflow_class)

    def salvar_log_transicao(self, status_evento, usuario, **kwargs):
        raise NotImplementedError('Deve criar um método salvar_log_transicao')

    @xworkflows.after_transition('sme_analisa_previamente')
    def _sme_analisa_previamente_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.AGUARDANDO_ANALISE_PREVIA_SME,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''))

    @xworkflows.after_transition('finaliza_area_insuficiente')
    def _finaliza_area_insuficiente_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.FINALIZADO_AREA_INSUFICIENTE,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False))

    @xworkflows.after_transition('finaliza_demanda_insuficiente')
    def _finaliza_demanda_insuficiente_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.FINALIZADO_DEMANDA_INSUFICIENTE,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False))

    @xworkflows.after_transition('finaliza_nao_atende_necessidades')
    def _finaliza_nao_atende_necessidades_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.FINALIZADO_NAO_ATENDE_NECESSIDADES,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False))

    @xworkflows.after_transition('envia_a_comapre')
    def _envia_a_comapre_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.ENVIADO_COMAPRE,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None))

    @xworkflows.after_transition('agenda_vistoria')
    def _agenda_vistoria_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.AGENDAMENTO_DA_VISTORIA,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None))

    @xworkflows.after_transition('aguarda_relatorio_vistoria')
    def _aguarda_relatorio_vistoria_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.AGUARDANDO_RELATORIO_DE_VISTORIA,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None))

    @xworkflows.after_transition('relatorio_vistoria')
    def _relatorio_vistoria_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.RELATORIO_VISTORIA,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None))

    @xworkflows.after_transition('aguarda_laudo_valor_locaticio')
    def _aguarda_laudo_valor_locaticio_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None))


    @xworkflows.after_transition('laudo_valor_locaticio')
    def _laudo_valor_locaticio_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.LAUDO_VALOR_LOCATICIO,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None))

    @xworkflows.after_transition('aprova_vistoria')
    def _aprova_vistoria_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.VISTORIA_APROVADA,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None))

    @xworkflows.after_transition('reprova_vistoria')
    def _reprova_vistoria_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.VISTORIA_REPROVADA,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None))

    @xworkflows.after_transition('envia_a_dre')
    def _envia_a_dre_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.ENVIADO_DRE,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None),
                                  processo_sei=kwargs.get('processo_sei', None),
                                  nome_da_unidade=kwargs.get('nome_da_unidade', None))

    @xworkflows.after_transition('finaliza_aprovado')
    def _finaliza_aprovado_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.FINALIZADO_APROVADO,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False))

    @xworkflows.after_transition('finaliza_reprovado')
    def _finaliza_reprovado_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.FINALIZADO_REPROVADO,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False))


    @xworkflows.after_transition('cancela')
    def _cancela_hook(self, *args, **kwargs):
        user = kwargs['user']
        self.salvar_log_transicao(status_evento=LogFluxoStatus.CANCELADO,
                                  usuario=user,
                                  justificativa=kwargs.get('justificativa', ''),
                                  email_enviado=kwargs.get('enviar_email', False),
                                  data_agendada=kwargs.get('data_agendada', None))
                                  
    @xworkflows.after_transition('reativa')
    def _reativa_hook(self, *args, **kwargs):
        logs = self.logs.all()
        for log in logs:
            log.anexos.all().delete()
        logs.delete()
        self.status = ImoveisWorkflow.initial_state
        self.save()

    class Meta:
        abstract = True
