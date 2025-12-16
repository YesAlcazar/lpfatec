from django.urls import path
from . import views

app_name = 'DocumentRest'
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_documento, name='upload_documento'),
    path('escolas/', views.listar_escolas, name='listar_escolas'),
    path('contato/', views.contato, name='contato'),
    path('ouvidoria/', views.ouvidoria, name='ouvidoria'),
    path('arquivos-a-vencer/', views.arquivos_a_vencer, name='arquivos_a_vencer'),
]