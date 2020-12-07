import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from rest_framework.exceptions import ValidationError


class Perfil(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"


class Secretaria(models.Model):
    nome = models.CharField("Nome", max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Secretaria"
        verbose_name_plural = "Secretarias"


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    perfil = models.ForeignKey(Perfil, null=True, on_delete=models.SET_NULL)
    secretaria = models.ForeignKey(Secretaria, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
