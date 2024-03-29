# Generated by Django 2.2.6 on 2021-02-15 04:29

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('imovel', '0024_auto_20210131_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='status',
            field=django_xworkflows.models.StateField(max_length=35, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='SOLICITACAO_REALIZADA', name='ImoveisWorkflow', states=['SOLICITACAO_REALIZADA', 'AGUARDANDO_ANALISE_PREVIA_SME', 'FINALIZADO_AREA_INSUFICIENTE', 'FINALIZADO_DEMANDA_INSUFICIENTE', 'FINALIZADO_NAO_ATENDE_NECESSIDADES', 'ENVIADO_COMAPRE', 'AGENDAMENTO_DA_VISTORIA', 'AGUARDANDO_RELATORIO_DE_VISTORIA', 'RELATORIO_VISTORIA', 'AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO', 'LAUDO_VALOR_LOCATICIO', 'VISTORIA_APROVADA', 'VISTORIA_REPROVADA', 'ENVIADO_DRE', 'FINALIZADO_APROVADO', 'FINALIZADO_REPROVADO', 'CANCELADO', 'REATIVADO'])),
        ),
    ]
