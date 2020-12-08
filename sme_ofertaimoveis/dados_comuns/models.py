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


class Subprefeitura(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)
    dre = models.ManyToManyField(DiretoriaRegional,
                                 related_name='subprefeituras',
                                 blank=True)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Subprefeitura"
        verbose_name_plural = "Subprefeituras"


class Distrito(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)
    subprefeitura = models.ForeignKey(Subprefeitura, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"


class Setor(models.Model):
    codigo = models.CharField("Código", max_length=4, null=True, blank=True)
    distrito = models.ForeignKey(Distrito, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.codigo}"

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
