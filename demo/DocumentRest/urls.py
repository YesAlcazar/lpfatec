from django.urls import path
from . import views

app_name = 'DocumentRest'
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_documento, name='upload_documento'),
    path('escolas/', views.listar_escolas, name='listar_escolas'),
]