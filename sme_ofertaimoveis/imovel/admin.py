from django.contrib import admin

from .models import ContatoImovel, Imovel, Proponente, SME_Contatos

admin.site.register(ContatoImovel)
admin.site.register(Proponente)
admin.site.register(Imovel)


@admin.register(SME_Contatos)
class SME_ContatosAdmin(admin.ModelAdmin):
    list_display = ("__str__", "ativo")
