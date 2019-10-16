from django.db import models
from django.core import validators

from .validators import phone_validation, cep_validation



class Contato(models.Model):

    name = models.CharField('Nome', max_length=255)
    email = models.CharField('E-mail', max_length=255, validators=[validators.EmailValidator()])
    telephone = models.CharField('Telefone', max_length=20, validators=[phone_validation])
    cellphone = models.CharField('Celular', max_length=20, validators=[phone_validation])
    criado_em = models.DateTimeField('Criado em', editable=False, auto_now_add=True)

    def __str__(self):
        return (f'{self.name} => {self.email} '
                f'{self.telephone} - {self.cellphone}')

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'


class Imovel(models.Model):

    contato = models.ForeignKey(Contato, on_delete=models.DO_NOTHING)
    address = models.CharField('Logradouro', max_length=255)
    neighborhood = models.CharField('Bairro', max_length=255)
    city = models.CharField('Cidade', max_length=20)
    state = models.CharField('Estado', max_length=20)
    cep = models.CharField('CEP', max_length=20)
    

    def __str__(self):
        return (f'{self.contato} => {self.address} '
                f'em {self.city} {self.state}')

    class Meta:
        verbose_name = 'Imovel'
        verbose_name_plural = 'Imoveis'
