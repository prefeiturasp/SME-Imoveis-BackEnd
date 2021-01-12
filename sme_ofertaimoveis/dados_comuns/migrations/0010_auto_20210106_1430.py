# Generated by Django 2.2.6 on 2021-01-06 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dados_comuns', '0009_auto_20201220_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diretoriaregional',
            options={'ordering': ('nome',), 'verbose_name': 'DRE', 'verbose_name_plural': 'DREs'},
        ),
        migrations.AlterModelOptions(
            name='distrito',
            options={'ordering': ('nome',), 'verbose_name': 'Distrito', 'verbose_name_plural': 'Distritos'},
        ),
        migrations.AlterModelOptions(
            name='secretaria',
            options={'ordering': ('nome',), 'verbose_name': 'Secretaria', 'verbose_name_plural': 'Secretarias'},
        ),
        migrations.AlterModelOptions(
            name='setor',
            options={'ordering': ('codigo',), 'verbose_name': 'Setor', 'verbose_name_plural': 'Setores'},
        ),
        migrations.AlterModelOptions(
            name='subprefeitura',
            options={'ordering': ('nome',), 'verbose_name': 'Subprefeitura', 'verbose_name_plural': 'Subprefeituras'},
        ),
    ]