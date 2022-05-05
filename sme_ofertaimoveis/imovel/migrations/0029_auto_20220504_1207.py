# Generated by Django 2.2.6 on 2022-05-04 15:07

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('imovel', '0028_auto_20210927_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='status',
            field=django_xworkflows.models.StateField(max_length=36, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='SOLICITACAO_REALIZADA', name='ImoveisWorkflow', states=['SOLICITACAO_REALIZADA', 'AGUARDANDO_ANALISE_PREVIA_SME', 'FINALIZADO_AREA_INSUFICIENTE', 'DEMANDA_INSUFICIENTE', 'FINALIZADO_NAO_ATENDE_NECESSIDADES', 'ENVIADO_PARA_SOLICITACAO_DE_VISTORIA', 'AGENDAMENTO_DA_VISTORIA', 'AGUARDANDO_RELATORIO_DE_VISTORIA', 'RELATORIO_VISTORIA', 'AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO', 'LAUDO_VALOR_LOCATICIO', 'VISTORIA_APROVADA', 'VISTORIA_REPROVADA', 'ENVIADO_DRE', 'FINALIZADO_APROVADO', 'FINALIZADO_REPROVADO', 'CANCELADO', 'REATIVADO'])),
        ),
    ]