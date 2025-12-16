from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import DocumentoForm
from .models import Documento, Escola
import base64
import binascii
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import re

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
            # Utiliza o get() para permitir capturar a exceção específica do Django caso não exista
            escola_instance = Escola.objects.get(cnpj=cnpj)
        except (binascii.Error, UnicodeDecodeError):
            # Captura erro de decodificação caso o hash da URL esteja malformado
            messages.error(request, "Link de acesso inválido.")
            return redirect('DocumentRest:home')
        except ObjectDoesNotExist:
            # Captura exceção específica do Django quando o objeto não é encontrado no banco
            messages.error(request, "Escola não encontrada.")
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

def contato(request):
    return render(request, 'contato.html')

def ouvidoria(request):
    return render(request, 'ouvidoria.html')

def arquivos_a_vencer(request):
    hoje = timezone.now().date()
    # Define o período de busca: até 3 meses no futuro a partir de hoje
    tres_meses_futuro = hoje + relativedelta(months=3)

    # Filtra documentos vencidos ou que vencerão nos próximos 3 meses
    documentos = Documento.objects.filter(
        data_vencimento__lte=tres_meses_futuro
    ).select_related('escola').order_by('data_vencimento')

    # Agrupa os documentos por escola para facilitar a exibição
    escolas_com_vencimentos = {}
    for doc in documentos:
        if doc.escola not in escolas_com_vencimentos:
            escolas_com_vencimentos[doc.escola] = []
        escolas_com_vencimentos[doc.escola].append(doc)

    context = {
        'escolas_com_vencimentos': escolas_com_vencimentos,
        'hoje': hoje,
    }
    return render(request, 'arquivos_a_vencer.html', context)

def status_documentos(request):
    # Busca todas as escolas e pré-carrega os documentos para otimizar a consulta
    escolas_qs = Escola.objects.all().prefetch_related('documentos')

    # Ordenação natural (Natural Sort) para que "Colégio 2" venha antes de "Colégio 10"
    def natural_keys(text):
        return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

    escolas = sorted(escolas_qs, key=lambda x: natural_keys(x.nome_fantasia))
    
    # Define os tipos de documentos obrigatórios (excluindo 'OUTRO')
    tipos_obrigatorios = [
        (code, label) for code, label in Documento.TipoDocumento.choices 
        if code != Documento.TipoDocumento.OUTRO
    ]
    tipos_obrigatorios.sort(key=lambda x: x[1])
    
    status_por_escola = []
    for escola in escolas:
        # Cria um conjunto com os tipos de documentos que a escola já enviou
        docs_enviados = set(escola.documentos.values_list('tipo_documento', flat=True))
        
        checklist = []
        entregues_count = 0
        
        for code, label in tipos_obrigatorios:
            entregue = code in docs_enviados
            if entregue:
                entregues_count += 1
            checklist.append({'label': label, 'entregue': entregue})
            
        status_por_escola.append({
            'escola': escola,
            'checklist': checklist,
            'entregues_count': entregues_count,
            'total_obrigatorio': len(tipos_obrigatorios)
        })
        
    return render(request, 'status_documentos.html', {'status_por_escola': status_por_escola})
