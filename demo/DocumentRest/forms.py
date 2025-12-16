from django import forms
from .models import Documento
from datetime import date
from dateutil.relativedelta import relativedelta # Requer: pip install python-dateutil

class DocumentoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Guarda a instância da escola, se for passada, e remove dos kwargs
        self.escola_instance = kwargs.pop('escola_instance', None)
        super().__init__(*args, **kwargs)

        # Se uma escola foi fornecida, pré-seleciona e desabilita o campo
        if self.escola_instance:
            self.initial['escola'] = self.escola_instance.pk
            self.fields['escola'].disabled = True
            self.fields['escola'].required = False

    # --- Novos campos para a data de vencimento ---
    TIPO_VENCIMENTO_CHOICES = [
        ('DATA', 'Data Específica'),
        ('ANO', 'Final do Ano (31/12)'),
    ]
    tipo_vencimento = forms.ChoiceField(
        choices=TIPO_VENCIMENTO_CHOICES,
        widget=forms.RadioSelect,
        label="Como deseja informar o vencimento?",
        required=True
    )

    vencimento_data = forms.DateField(
        label="Data de Vencimento Específica",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

    current_year = date.today().year
    YEAR_CHOICES = [(str(y), str(y)) for y in range(current_year, current_year + 6)]
    vencimento_ano = forms.ChoiceField(
        choices=[('', 'Selecione o ano')] + YEAR_CHOICES,
        label="Ano de Vencimento",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Documento
        fields = [
            'escola',
            'arquivo',
            'tipo_documento',
            'outro_tipo_documento',
            'responsavel_upload',
        ]
        widgets = {
            'escola': forms.Select(attrs={'class': 'form-control'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo_documento'}),
            'outro_tipo_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especifique o tipo do documento'}),
            'responsavel_upload': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        escola = cleaned_data.get('escola')

        # Se o campo escola foi desabilitado, seu valor não vem no POST.
        # Nós o adicionamos de volta aos dados validados.
        if not escola and self.escola_instance:
            cleaned_data['escola'] = self.escola_instance
        # Garante que o campo é obrigatório no caso de um upload geral
        elif not escola and not self.escola_instance:
            self.add_error('escola', 'Este campo é obrigatório.')

        tipo_documento = cleaned_data.get("tipo_documento")
        outro_tipo_documento = cleaned_data.get("outro_tipo_documento")

        if tipo_documento == Documento.TipoDocumento.OUTRO and not outro_tipo_documento:
            self.add_error('outro_tipo_documento', "Este campo é obrigatório quando o tipo de documento é 'Outro'.")
        
        # --- Validação da data de vencimento ---
        tipo_vencimento = cleaned_data.get('tipo_vencimento')
        vencimento_data = cleaned_data.get('vencimento_data')
        vencimento_ano = cleaned_data.get('vencimento_ano')
        
        data_vencimento_final = None

        if tipo_vencimento == 'DATA':
            if not vencimento_data:
                self.add_error('vencimento_data', 'Este campo é obrigatório ao selecionar "Data Específica".')
            else:
                # Validação: não pode ser superior a 5 anos no futuro
                if vencimento_data > (date.today() + relativedelta(years=5)):
                    self.add_error('vencimento_data', 'A data de vencimento não pode ser superior a 5 anos no futuro.')
                else:
                    data_vencimento_final = vencimento_data
        elif tipo_vencimento == 'ANO':
            if not vencimento_ano:
                self.add_error('vencimento_ano', 'Este campo é obrigatório ao selecionar "Final do Ano".')
            else:
                data_vencimento_final = date(int(vencimento_ano), 12, 31)

        if data_vencimento_final:
            cleaned_data['data_vencimento'] = data_vencimento_final

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.data_vencimento = self.cleaned_data.get('data_vencimento')
        if commit:
            instance.save()
        return instance