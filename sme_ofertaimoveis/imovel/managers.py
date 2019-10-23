from django.db import models


class SME_ContatosManager(models.Manager):
    def get_contatos_ativos(self):
        return self.filter(ativo=True)
