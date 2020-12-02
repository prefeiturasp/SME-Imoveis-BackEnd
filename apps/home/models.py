# -*- coding: utf-8 -*-
from django.db import models
from django.core import validators
from .validators import (
    cep_validation, cpf_cnpj_validation, name_validation, phone_validation
)
from commom.choices import CHOICE_SIM_NAO


class TypeBidders(models.Model):
    pk_type_bidders = models.AutoField('Código', primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Nome')
    insert_date = models.DateTimeField(
        "Criado em", editable=False, auto_now_add=True
    )
    update_date = models.DateTimeField(
        "Alterado em", editable=False, auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sme_type_bidders'
        verbose_name = 'Tipo de Proponente'
        verbose_name_plural = 'Tipos de Proponentes'


class Bidders(models.Model):
    pk_bidders = models.CharField(
        "CPF / CNPJ", max_length=20, validators=[cpf_cnpj_validation], primary_key=True
    )
    fk_type_bidders = models.ForeignKey(
        TypeBidders, models.PROTECT, verbose_name='Tipo'
    )
    name = models.CharField(
        "Nome", max_length=255, validators=[name_validation]
    )
    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()]
        , blank=True, null=True, default=""
    )
    phone = models.CharField(
        "Telefone", max_length=20, validators=[phone_validation]
        , blank=True, null=True, default=""
    )
    cel_phone = models.CharField(
        "Celular", max_length=20, validators=[phone_validation]
        , blank=True, null=True, default=""
    )
    insert_date = models.DateTimeField(
        "Criado em", editable=False, auto_now_add=True
    )
    update_date = models.DateTimeField(
        "Alterado em", editable=False, auto_now=True
    )

    def __str__(self):
        return f"{self.name}: {self.email} - {self.phone}"

    class Meta:
        db_table = 'sme_bidders'
        verbose_name = "Home Proponente"
        verbose_name_plural = "Home Proponentes"


class BiddersBuildings(models.Model):

    fk_bidders = models.ForeignKey(Bidders, models.CASCADE, verbose_name='Proponente')

    # fk_countries = models.ForeignKey(Countries, models.CASCADE, verbose_name='País')
    # fk_provinces = models.ForeignKey(Provinces, models.CASCADE, verbose_name='Estado')
    # fk_cities = models.ForeignKey(Cities, models.CASCADE, verbose_name='Município')
    cep = models.CharField("CEP", max_length=20, validators=[cep_validation])
    address = models.CharField("Logradouro", max_length=255)
    quarter = models.CharField("Bairro", max_length=255)
    number = models.CharField("Número", max_length=255)
    complement = models.CharField(
        "Complemento", max_length=255, null=True, blank=True
    )
    latitude = models.CharField("Latitude", max_length=20)
    longitude = models.CharField("longitude", max_length=20)
    number_iptu = models.CharField("Número IPTU", max_length=20)
    insert_date = models.DateTimeField(
        "Criado em", editable=False, auto_now_add=True
    )
    update_date = models.DateTimeField(
        "Alterado em", editable=False, auto_now=True
    )

    # @property
    # def planta_fotos(self):
    #     return self.plantafoto_set.all()

    @property
    def protocolo(self):
        return f"{self.id:03d}/{str(self.insert_date.year)}"

    @property
    def name(self):
        return self.fk_bidders.name

    def __str__(self):
        return f"{self.name}\n{self.address}"

    class Meta:
        db_table = 'sme_bidders_buildings'
        verbose_name = "Home Imóvel"
        verbose_name_plural = "Home Imóveis"


class BiddersBuildingsDocsImages(models.Model):
    TYPE_DOCUMENTOS = (
        (1, 'Fotos da Fachada'),
        (2, 'Fotos do Ambiente Interno'),
        (3, 'Cópia do IPTU ou ITR'),
        (4, 'Cópia da Planta ou Croqui'),
    )

    TYPE_FILE = (
        (1, 'Imagem'),
        (2, 'Documento')
    )

    fk_bidders_buildings = models.ForeignKey(
        BiddersBuildings, on_delete=models.CASCADE, verbose_name='Imóvel'
    )

    document = models.FileField('Documetos/Imagens')
    flag_type_docs = models.SmallIntegerField(
        'Tipo Documento', choices=TYPE_DOCUMENTOS, blank=True, null=True
    )
    flag_type_file = models.SmallIntegerField(
        'Tipo Arquivo', choices=TYPE_FILE, blank=True, null=True
    )
    insert_date = models.DateTimeField(
        "Criado em", editable=False, auto_now_add=True
    )
    update_date = models.DateTimeField(
        "Alterado em", editable=False, auto_now=True
    )

    @property
    def name(self):
        return self.fk_bidders_buildings.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'sme_bidders_buildings_docs_imgs'
        verbose_name = "Imóvel Doc & Imagem"
        verbose_name_plural = "Imóvel Docs & Imagens"
