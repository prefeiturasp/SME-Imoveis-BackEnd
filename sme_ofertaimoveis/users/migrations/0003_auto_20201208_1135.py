# Generated by Django 2.2.6 on 2020-12-08 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dados_comuns', '0001_initial'),
        ('users', '0002_auto_20201207_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dados_comuns.DiretoriaRegional'),
        ),
        migrations.AddField(
            model_name='user',
            name='secretaria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dados_comuns.Secretaria'),
        ),
    ]
