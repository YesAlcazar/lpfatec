from django.db import models

# Create your models here.
# Model para a Escola
class Escola(models.Model):
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social")
    nome_fantasia = models.CharField(max_length=255, verbose_name="Nome Fantasia")
    endereco = models.TextField(verbose_name="Endereço Principal")
    # Adicionar validador para CNPJ seria uma boa prática em forms.py ou com uma biblioteca externa
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ") # Formato: XX.XXX.XXX/XXXX-XX

    def __str__(self):
        return self.nome_fantasia

    class Meta:
        verbose_name = "Escola"
        verbose_name_plural = "Escolas"

# Model para Unidades da Escola (caso haja múltiplos endereços)
class Unidade(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='unidades', verbose_name="Escola")
    nome = models.CharField(max_length=100, verbose_name="Nome da Unidade") # Ex: "Unidade Centro"
    endereco = models.TextField(verbose_name="Endereço")

    def __str__(self):
        return f"{self.escola.nome_fantasia} - {self.nome}"

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"

# Model para Contatos da Escola
class Contato(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='contatos', verbose_name="Escola")
    nome = models.CharField(max_length=100, verbose_name="Nome do Contato")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"

# Model principal para o Documento
class Documento(models.Model):
    class TipoDocumento(models.TextChoices):
        AVCB = 'AVCB', 'AVCB (Auto de Vistoria do Corpo de Bombeiros)'
        ALVARA = 'ALVARA', 'Alvará de Funcionamento'
        PLANO_ENSINO = 'PLANO_ENSINO', 'Plano de Ensino'
        CONTRATO = 'CONTRATO', 'Contrato'
        OUTRO = 'OUTRO', 'Outro'

    arquivo = models.FileField(upload_to='documentos/', verbose_name="Arquivo")
    tipo_documento = models.CharField(
        max_length=20,
        choices=TipoDocumento.choices,
        default=TipoDocumento.OUTRO,
        verbose_name="Tipo de Documento"
    )
    outro_tipo_documento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Especificar (se 'Outro')"
    )
    escola = models.ForeignKey(Escola, on_delete=models.PROTECT, related_name='documentos', verbose_name="Escola")
    responsavel_upload = models.CharField(max_length=100, verbose_name="Responsável pelo Upload")
    data_hora_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora de Envio")

    def __str__(self):
        tipo_display = self.get_tipo_documento_display()
        if self.tipo_documento == self.TipoDocumento.OUTRO and self.outro_tipo_documento:
            return f"{tipo_display}: {self.outro_tipo_documento} - {self.escola.nome_fantasia}"
        return f"{tipo_display} - {self.escola.nome_fantasia}"

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
