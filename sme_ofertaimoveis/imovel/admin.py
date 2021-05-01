from django.contrib import admin
from django.utils.html import format_html

from .models import ContatoImovel, Imovel, Proponente, SME_Contatos, PlantaFoto, DemandaImovel


@admin.register(SME_Contatos)
class SME_ContatosAdmin(admin.ModelAdmin):
    list_display = ("__str__", "ativo")


@admin.register(Proponente)
class ProponenteAdmin(admin.ModelAdmin):
    fields = ('nome', 'cpf_cnpj', 'email', 'telefone', 'tipo_proponente')

    list_display = ('nome', 'cpf_cnpj', 'email', 'telefone', 'situacao', 'tipo_proponente')
    list_filter = ('situacao', 'tipo_proponente')




@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ("protocolo", 'proponente', 'contato', 'cep', 'endereco', 'excluido')
    search_fields = ('cep', 'endereco')
    fields = ("protocolo", 'show_proponente', 'show_contato', 'area_construida', 'cidade', 'uf', 'cep', "endereco", "bairro", 'numero', 'complemento',
              'numero_iptu', 'criado_em', 'observacoes', 'setor', 'secretaria', 'status', 'latitude', 'longitude', 'excluido', 'situacao_duplicidade')
    list_filter = ('excluido', 'situacao_duplicidade')
    readonly_fields = ("protocolo", 'show_proponente', 'show_contato', 'criado_em')

    def show_proponente(self, obj):
        return format_html("<a href='/api/admin/imovel/proponente/{id}/change'>{url}</a>", id=obj.proponente.id,
                           url=obj.proponente)

    show_proponente.short_description = "Proponente"

    def show_contato(self, obj):
        return format_html("<a href='/api/admin/imovel/contatoimovel/{id}/change'>{url}</a>", id=obj.contato.id,
                           url=obj.contato)

    show_contato.short_description = "Contato"

    class AnexosInline(admin.TabularInline):
        model = PlantaFoto
        extra = 0

    inlines = [
        AnexosInline,
    ]


admin.site.register(ContatoImovel)
admin.site.register(DemandaImovel)
