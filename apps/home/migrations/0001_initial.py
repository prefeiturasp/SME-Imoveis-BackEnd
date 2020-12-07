# Generated by Django 2.2.6 on 2020-12-07 14:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bidders',
            fields=[
                ('pk_bidders', models.CharField(max_length=20, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='Digite o CPF ou CNPJ no formato XX.XXX.XXX/XXXX-XX ou XXX.XXX.XXX-XX.', regex='(^\\d{3}\\.\\d{3}\\.\\d{3}\\-\\d{2}$)|(^\\d{2}\\.\\d{3}\\.\\d{3}\\/\\d{4}\\-\\d{2}$)')], verbose_name='CPF / CNPJ')),
                ('name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Digite o nome com no mínimo 2 palavras com 3 caracteres cada', regex='^([A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\\S]{3,}\\w)|([A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\\S]{3,}\\w+)')], verbose_name='Nome')),
                ('email', models.CharField(blank=True, default='', max_length=255, null=True, validators=[django.core.validators.EmailValidator()], verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, default='', max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Digite o telefone no formato (XX) 12345-6789. Entre 8 ou 9 digitos', regex='^\\(\\d{2}\\) [\\d\\-]{9,10}$')], verbose_name='Telefone')),
                ('cel_phone', models.CharField(blank=True, default='', max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Digite o telefone no formato (XX) 12345-6789. Entre 8 ou 9 digitos', regex='^\\(\\d{2}\\) [\\d\\-]{9,10}$')], verbose_name='Celular')),
                ('insert_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
            ],
            options={
                'verbose_name': 'Home Proponente',
                'verbose_name_plural': 'Home Proponentes',
                'db_table': 'sme_bidders',
            },
        ),
        migrations.CreateModel(
            name='BiddersBuildings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Digite o CEP no formato XXXXX-XXX. Com 8 digitos', regex='^\\d{5}-\\d{3}$')], verbose_name='CEP')),
                ('address', models.CharField(max_length=255, verbose_name='Logradouro')),
                ('quarter', models.CharField(max_length=255, verbose_name='Bairro')),
                ('number', models.CharField(max_length=255, verbose_name='Número')),
                ('complement', models.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
                ('latitude', models.CharField(max_length=20, verbose_name='Latitude')),
                ('longitude', models.CharField(max_length=20, verbose_name='longitude')),
                ('number_iptu', models.CharField(max_length=20, verbose_name='Número IPTU')),
                ('insert_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('fk_bidders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Bidders', verbose_name='Proponente')),
            ],
            options={
                'verbose_name': 'Home Imóvel',
                'verbose_name_plural': 'Home Imóveis',
                'db_table': 'sme_bidders_buildings',
            },
        ),
        migrations.CreateModel(
            name='TypeBidders',
            fields=[
                ('pk_type_bidders', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('insert_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
            ],
            options={
                'verbose_name': 'Tipo de Proponente',
                'verbose_name_plural': 'Tipos de Proponentes',
                'db_table': 'sme_type_bidders',
            },
        ),
        migrations.CreateModel(
            name='BiddersBuildingsDocsImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='', verbose_name='Documetos/Imagens')),
                ('flag_type_docs', models.SmallIntegerField(blank=True, choices=[(1, 'Fotos da Fachada'), (2, 'Fotos do Ambiente Interno'), (3, 'Cópia do IPTU ou ITR'), (4, 'Cópia da Planta ou Croqui')], null=True, verbose_name='Tipo Documento')),
                ('flag_type_file', models.SmallIntegerField(blank=True, choices=[(1, 'Imagem'), (2, 'Documento')], null=True, verbose_name='Tipo Arquivo')),
                ('insert_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('fk_bidders_buildings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.BiddersBuildings', verbose_name='Imóvel')),
            ],
            options={
                'verbose_name': 'Imóvel Doc & Imagem',
                'verbose_name_plural': 'Imóvel Docs & Imagens',
                'db_table': 'sme_bidders_buildings_docs_imgs',
            },
        ),
        migrations.AddField(
            model_name='bidders',
            name='fk_type_bidders',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.TypeBidders', verbose_name='Tipo'),
        ),
    ]
