import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from sme_ofertaimoveis.dados_comuns.models import Secretaria, Setor


class Perfil(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    perfil = models.ForeignKey(Perfil, null=True, blank=True, on_delete=models.SET_NULL)
    secretaria = models.ForeignKey(Secretaria, null=True, blank=True, on_delete=models.SET_NULL)
    setor = models.ForeignKey(Setor, null=True, blank=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
