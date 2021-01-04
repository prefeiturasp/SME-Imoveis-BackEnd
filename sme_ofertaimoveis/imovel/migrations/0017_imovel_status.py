# Generated by Django 2.2.6 on 2020-12-19 18:03

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('imovel', '0016_auto_20201208_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='imovel',
            name='status',
            field=django_xworkflows.models.StateField(max_length=35, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='AGUARDANDO_ANALISE_PREVISA_SME', name='ImoveisWorkflow', states=['AGUARDANDO_ANALISE_PREVISA_SME', 'ENVIADO_COMAPRE', 'AGUARDANDO_RELATORIO_DE_VISTORIA', 'AGUARDANDO_LAUDO_DE_VALOR_LOCATICIO', 'APROVADO', 'ENVIADO_DRE', 'FINALIZADO', 'CANCELADO'])),
        ),
    ]
