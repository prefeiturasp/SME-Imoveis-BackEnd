from django.db import models


class Secretaria(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Secretaria"
        verbose_name_plural = "Secretarias"


class DiretoriaRegional(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)
    sigla = models.CharField("Sigla", max_length=2)
    codigo_eol = models.CharField("Código EOL", max_length=6)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "DRE"
        verbose_name_plural = "DREs"
