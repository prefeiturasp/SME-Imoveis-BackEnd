from django.core import validators


phone_validation = validators.RegexValidator(
     regex=r'^\(\d{2}\) [\d-]{9,10}$', 
     message="Digite o telefone no formato (XX) 12345-6789. Entre 8 ou 9 digitos")


cep_validation = validators.RegexValidator(
     regex=r'^\d{5}-\d{3}$', 
     message="Digite o CEP no formato XXXXX-XXX. Com 8 digitos")
