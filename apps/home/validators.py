#-*- coding: utf-8 -*-
from django.core import validators

name_validation = validators.RegexValidator(
    #deve conter pelo menos dois nomes com 3 carateres cada
    regex=r"^([A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\S]{3,}\w)|([A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\S]{3,}\w+)",
    message="Digite o nome com no mínimo 2 palavras com 3 caracteres cada",
)

phone_validation = validators.RegexValidator(
    regex=r"^\(\d{2}\) [\d\-]{9,10}$",
    message="Digite o telefone no formato (XX) 12345-6789. Entre 8 ou 9 digitos",
)

cep_validation = validators.RegexValidator(
    regex=r"^\d{5}-\d{3}$", message="Digite o CEP no formato XXXXX-XXX. Com 8 digitos"
)

cpf_cnpj_validation = validators.RegexValidator(
    regex=r"(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)|(^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$)",
    message="Digite o CPF ou CNPJ no formato XX.XXX.XXX/XXXX-XX ou XXX.XXX.XXX-XX.",
)
