import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.urls import reverse

from ..dados_comuns.models import Secretaria, Setor
from ..dados_comuns.utils import url_configs, send_email
from ..imovel.tasks import send_email_


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

    def enviar_email_recuperacao_senha(self):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self)
        content = {'uuid': self.uuid, 'confirmation_key': token}
        """
        send_email_.delay(
            subject="Recuperação de senha",
            template="recuperar_senha",
            data={'link': url_configs("RECUPERAR_SENHA", content)},
            to_email=self.email
        )
        """
        # sem celery
        send_email(
            subject="Recuperação de senha",
            template="recuperar_senha",
            data={'link': url_configs("RECUPERAR_SENHA", content)},
            to_email=self.email,
        )

    def atualiza_senha(self, senha, token):
        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(self, token):
            self.set_password(senha)
            self.save()
            return True
        return False

    class Meta:
        ordering = ("first_name", "last_name",)
