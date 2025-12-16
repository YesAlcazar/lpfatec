from django import forms
from .models import Documento

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
        return cleaned_data