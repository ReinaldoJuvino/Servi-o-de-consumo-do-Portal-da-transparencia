from django.contrib import admin

# Register your models here.
from prestcontas_api.models import TipoOrgao, PalavraChave, TipoInstrumento, TipoEntidade, Orgao, Entidade, Instrumento

admin.site.register(TipoOrgao)
admin.site.register(PalavraChave)
admin.site.register(TipoInstrumento)
admin.site.register(TipoEntidade)
admin.site.register(Orgao)
admin.site.register(Entidade)
admin.site.register(Instrumento)
