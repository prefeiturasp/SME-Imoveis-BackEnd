from django.contrib import admin
from django.utils.html import format_html

from .models import ContatoImovel, Imovel, Proponente, SME_Contatos, PlantaFoto


@admin.register(SME_Contatos)
class SME_ContatosAdmin(admin.ModelAdmin):
    list_display = ("__str__", "ativo")


@admin.register(Proponente)
class ProponenteAdmin(admin.ModelAdmin):
    fields = ('get_tipo', 'nome', 'cpf_cnpj', 'email', 'telefone')

    list_display = ('nome', 'cpf_cnpj', 'email', 'telefone', 'situacao')
    list_filter = ('situacao', 'fk_tipo_proponente')

    def get_tipo(self, obj):
        return obj.TYPES[int(obj.tipo)][1]

    get_tipo.short_description = 'Tipo'


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ("protocolo", 'proponente', 'contato', 'cep', 'endereco')
    search_fields = ('cep', 'endereco')
    fields = ("protocolo", 'show_proponente', 'show_contato', 'cep', "endereco", "bairro", 'numero', 'complemento',
              'numero_iptu', 'criado_em')
    readonly_fields = ("protocolo", 'show_proponente', 'show_contato', 'criado_em')

    def show_proponente(self, obj):
        return format_html("<a href='/api/admin/imovel/proponente/{id}/change'>{url}</a>", id=obj.proponente.id,
                           url=obj.proponente)

    show_proponente.short_description = "Proponente"

    def show_contato(self, obj):
        return format_html("<a href='/api/admin/imovel/contatoimovel/{id}/change'>{url}</a>", id=obj.contato.id,
                           url=obj.contato)

    show_contato.short_description = "Contato"

    class PlantaFotoInline(admin.TabularInline):
        model = PlantaFoto
        extra = 0

    inlines = [
        PlantaFotoInline,
    ]


admin.site.register(ContatoImovel)
