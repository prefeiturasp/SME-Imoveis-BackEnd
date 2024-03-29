# Generated by Django 2.2.6 on 2020-12-20 18:43

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('imovel', '0017_imovel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='status',
            field=django_xworkflows.models.StateField(max_length=35, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='SOLICITACAO_REALIZADA', name='ImoveisWorkflow', states=['SOLICITACAO_REALIZADA', 'AGUARDANDO_ANALISE_PREVISA_SME', 'ENVIADO_COMAPRE', 'AGUARDANDO_RELATORIO_DE_VISTORIA', 'AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO', 'APROVADO', 'ENVIADO_DRE', 'FINALIZADO', 'CANCELADO'])),
        ),
    ]
