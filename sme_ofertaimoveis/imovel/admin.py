from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html

from .models import ContatoImovel, Imovel, Proponente, SME_Contatos, PlantaFoto, DemandaImovel
from .utils import (
    atualiza_imoveis_endereco_duplicado,
    atualiza_imoveis_iptu_duplicado
)

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
    list_display = ("protocolo", 'proponente', 'contato', 'cep', 'endereco')
    search_fields = ('cep', 'endereco')
    fields = ("protocolo", 'show_proponente', 'show_contato', 'area_construida', 'cidade', 'uf', 'cep', "endereco", "bairro", 'numero', 'complemento',
              'numero_iptu', 'criado_em', 'observacoes', 'setor', 'secretaria', 'status')
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

    change_list_template = 'imovel/html/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('atualiza_situacao/', self.admin_site.admin_view(
                self.atualiza_situacao, cacheable=False)),
        ]
        return my_urls + urls

    def atualiza_situacao(self, request):
        atualiza_imoveis_endereco_duplicado()
        atualiza_imoveis_iptu_duplicado()
        messages.add_message(
            request,
            messages.INFO,
            'Atualização de situação realizada com sucesso.'
        )
        return redirect('admin:imovel_imovel_changelist')




admin.site.register(ContatoImovel)
admin.site.register(DemandaImovel)
