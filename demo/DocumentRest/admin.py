from django.contrib import admin
# from .models import TodoItem
from .models import Escola, Unidade, Contato, Documento

# Register your models here.

# admin.site.register(TodoItem)
@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'razao_social', 'cnpj')
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj')

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'escola')
    list_filter = ('escola',)
    search_fields = ('nome',)

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'escola')
    list_filter = ('escola',)
    search_fields = ('nome', 'email')

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'responsavel_upload', 'data_hora_envio')
    list_filter = ('tipo_documento', 'escola', 'data_hora_envio')
    search_fields = ('responsavel_upload', 'escola__nome_fantasia')
    date_hierarchy = 'data_hora_envio'