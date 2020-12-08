from django.contrib import admin

from .models import DiretoriaRegional, Distrito, Secretaria, Setor, Subprefeitura

admin.site.register(DiretoriaRegional)
admin.site.register(Distrito)
admin.site.register(Secretaria)
admin.site.register(Setor)
admin.site.register(Subprefeitura)
