from django.contrib import admin

from .models import ContatoImovel, Imovel, Proponente, SME_Contatos, PlantaFoto


@admin.register(SME_Contatos)
class SME_ContatosAdmin(admin.ModelAdmin):
    list_display = ("__str__", "ativo")


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    
    class PlantaFotoInline(admin.TabularInline):
        model = PlantaFoto
        extra = 0

    inlines = [
        PlantaFotoInline,
    ]

admin.site.register(ContatoImovel)
admin.site.register(Proponente)
