# Generated by Django 2.2.6 on 2021-02-12 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dados_comuns', '0012_auto_20210205_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='logfluxostatus',
            name='nome_da_unidade',
            field=models.TextField(blank=True, null=True, verbose_name='Nome da unidade'),
        ),
        migrations.AddField(
            model_name='logfluxostatus',
            name='processo_sei',
            field=models.TextField(blank=True, null=True, verbose_name='Numero processo SEI'),
        ),
    ]
