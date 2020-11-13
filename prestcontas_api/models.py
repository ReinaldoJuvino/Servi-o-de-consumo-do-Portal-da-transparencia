from django.db import models
from ckeditor.fields import RichTextField


class TipoOrgao(models.Model):
    descricao = models.CharField(u'Descriçao', max_length=100)

    def __str__(self):
        return self.descricao


class PalavraChave(models.Model):
    palavra = models.CharField(max_length=255)

    def __str__(self):
        return self.palavra


class TipoInstrumento(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao


class TipoEntidade(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao


class Orgao(models.Model):
    tipo = models.ForeignKey(TipoOrgao, on_delete=models.PROTECT, related_name='orgao')
    nome = models.CharField(u'Nome', max_length=255)
    cnpj = models.CharField(u'CNPJ', max_length=18, blank=True, null=True)

    cep = models.CharField(max_length=10, null=True, blank=True)
    logradouro = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=10, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    #brasao = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Entidade(models.Model):
    tipo = models.ForeignKey(TipoEntidade, on_delete=models.PROTECT, null=True)
    cnpj = models.CharField(u'CNPJ', max_length=255, unique=True, null=True, blank=True)
    cpf = models.CharField(u'CPF', max_length=25, unique=True, null=True, blank=True)
    razao = models.CharField(u'Razão Social', max_length=255, unique=True)
    codigo_municipio = models.PositiveIntegerField(u'código do município', blank=True, null=True)

    cep = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=10)
    numero = models.CharField(max_length=50)
    #brasao = models.ImageField(blank=True, null=True)

    date_registro = models.DateTimeField(auto_now_add=True)
    ultima_modificacao = models.DateTimeField(auto_now=True)

    email_caixa_cadastrado = models.BooleanField(default=False)
    cliente_ativo = models.BooleanField(default=True)
    situacao_adimplencia = models.BooleanField(default=False, blank=True)

    sede = models.BooleanField(default=False)
    nome_fantasia = models.CharField(u'Nome', max_length=255, unique=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    telefone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.municipio


class Instrumento(models.Model):
    entidade = models.ForeignKey(Entidade, on_delete=models.PROTECT, null=True)
    tipo = models.ForeignKey(TipoInstrumento, on_delete=models.PROTECT, verbose_name='Tipo Instrumento')
    #campo interno
    palavra_chave = models.ForeignKey(PalavraChave, on_delete=models.PROTECT, null=True)

    numero_operacao = models.CharField(max_length=255, verbose_name='Numero/Operaçao', null=True, blank=True,
                                       default="N/A")
    siafi_sicony = models.CharField(max_length=255, verbose_name='SIAFI/SICONV', null=True, blank=True)

    concedente = models.ForeignKey(Orgao, on_delete=models.PROTECT, related_name='orgao_concedente_instrumento')
    interveniente = models.ForeignKey(Orgao, on_delete=models.PROTECT, related_name='orgao_interveniente_instrumento',
                                      null=True, blank=True)

    inicio = models.DateField(null=True, blank=True)
    termino = models.DateField(null=True, blank=True)

    ano = models.IntegerField(null=True)
    prorrogado = models.DateField(null=True, blank=True)

    repasse = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    contrapartida = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)

    aditivo_valor_adicao = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    aditivo_valor_supressao = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    ultima_modificacao = models.DateTimeField(auto_now=True)

    objeto = RichTextField(null=True, blank=True)