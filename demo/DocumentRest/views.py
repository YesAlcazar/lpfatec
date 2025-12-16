from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DocumentoForm
from .models import Documento, Escola
import base64

# Create your views here.
def home(request):
    documentos_recentes = Documento.objects.order_by('-data_hora_envio')[:10]
    return render(request, 'home.html', {'documentos_recentes': documentos_recentes})

def upload_documento(request):
    escola_instance = None
    escola_id_b64 = request.GET.get('id')

    if escola_id_b64:
        try:
            # Decodifica o ID da URL para obter o CNPJ e buscar a escola
            cnpj = base64.b64decode(escola_id_b64).decode('utf-8')
            escola_instance = get_object_or_404(Escola, cnpj=cnpj)
        except Exception:
            messages.error(request, "Link de acesso inválido ou escola não encontrada.")
            return redirect('DocumentRest:home')

    if request.method == 'POST':
        # Passa a instância da escola para o form lidar com o campo desabilitado
        form = DocumentoForm(request.POST, request.FILES, escola_instance=escola_instance)
        if form.is_valid():
            form.save()
            responsavel = form.cleaned_data['responsavel_upload']
            messages.success(request, 'Documento enviado com sucesso!')
            
            # Cria a resposta de redirecionamento para poder adicionar o cookie
            response = redirect('DocumentRest:home')
            # Define o cookie com o nome do responsável por 1 ano
            response.set_cookie('ultimo_responsavel', responsavel, max_age=365*24*60*60)
            return response
    else:
        # Preenche o nome do responsável com o valor do cookie, se existir
        initial_data = {'responsavel_upload': request.COOKIES.get('ultimo_responsavel', '')}
        form = DocumentoForm(initial=initial_data, escola_instance=escola_instance)
    
    return render(request, 'upload.html', {'form': form, 'escola_selecionada': escola_instance})

def listar_escolas(request):
    escolas = Escola.objects.all().order_by('nome_fantasia')
    for escola in escolas:
        # Gera o código de acesso Base64 para cada escola
        escola.access_code = base64.b64encode(escola.cnpj.encode('utf-8')).decode('utf-8')
    return render(request, 'escolas_list.html', {'escolas': escolas})
