import datetime
from django.db import models
from django.core import validators

from .validators import phone_validation, cep_validation, cpf_cnpj_validation
from .managers import SME_ContatosManager


class SME_Contatos(models.Model):
    nome = models.CharField("Nome", max_length=255)
    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()]
    )
    ativo = models.BooleanField("Esta ativo", default=True)
    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    objects = SME_ContatosManager()

    def __str__(self):
        return f"{self.nome} => {self.email}"

    class Meta:
        verbose_name = "Contato Prefeitura"
        verbose_name_plural = "Contatos Prefeitura"


class Proponente(models.Model):

    IMOBILIARIA = 1
    PROCURADOR = 2
    ONG = 3
    OUTRO = 4

    TYPES = (
        (0, "----SELECIONE-----"),
        (IMOBILIARIA, "Imobiliária"),
        (PROCURADOR , "Procurador"),
        (ONG , "Ong"),
        (OUTRO , "Outro"),
    )

    tipo = models.PositiveSmallIntegerField("Tipo", choices=TYPES, default=OUTRO)
    nome = models.CharField("Nome", max_length=255, blank=True, null=True)
    cpf_cnpj = models.CharField(
        "CPF / CNPJ", max_length=20, validators=[cpf_cnpj_validation]
        , blank=True, null=True, default=""
    )
    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()]
        , blank=True, null=True, default=""
    )
    telefone = models.CharField(
        "Telefone", max_length=20, validators=[phone_validation]
        , blank=True, null=True, default=""
    )
    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    def __str__(self):
        return f"{self.nome} => {self.email} " f"{self.telefone}"

    class Meta:
        verbose_name = "Proponente"
        verbose_name_plural = "Proponentes"


class ContatoImovel(models.Model):

    nome = models.CharField("Nome", max_length=255)
    cpf_cnpj = models.CharField("CPF / CNPJ", max_length=20)
    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()]
        , blank=True, null=True, default=""
    )
    telefone = models.CharField(
        "Telefone", max_length=20, validators=[phone_validation]
        , blank=True, null=True, default=""
    )
    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    def __str__(self):
        return f"{self.nome} => {self.cpf_cnpj}"

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"


class Imovel(models.Model):

    proponente = models.ForeignKey(Proponente, on_delete=models.DO_NOTHING, blank=True, null=True)
    contato = models.ForeignKey(ContatoImovel, on_delete=models.DO_NOTHING)

    cep = models.CharField("CEP", max_length=20, validators=[cep_validation])
    endereco = models.CharField("Logradouro", max_length=255)
    bairro = models.CharField("Bairro", max_length=255)
    numero = models.CharField("Numero", max_length=255)
    complemento = models.CharField("Complemento", max_length=255, null=True, blank=True)

    latitude = models.CharField("Latitude", max_length=255)
    longitude = models.CharField("longitude", max_length=255)
    numero_iptu = models.CharField("Numero IPTU", max_length=20, blank=True, default="")

    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    @property
    def planta_fotos(self):
        return self.plantafoto_set.all()

    @property
    def protocolo(self):
        return "{:03d}".format(self.id) + "/" + str(self.criado_em.year)

    def __str__(self):
        return f"{self.contato} => {self.endereco}"

    class Meta:
        verbose_name = "Imovel"
        verbose_name_plural = "Imoveis"


class PlantaFoto(models.Model):

    imovel = models.ForeignKey(Imovel, on_delete=models.DO_NOTHING)
    planta = models.FileField()
    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)
