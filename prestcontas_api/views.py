import json
from datetime import datetime
from time import sleep

from django.shortcuts import render
import requests
from prestcontas_api.models import Entidade, Instrumento, TipoInstrumento, TipoOrgao, Orgao


def index(request):
    get_entidade = Entidade.objects.all()
    headers = {'chave-api-dados': '99d565aeacc2e7414dadd7a377f17417', 'Accept': "*/*"}
    url_base = 'http://www.portaltransparencia.gov.br/api-de-dados'

    for entidade in get_entidade:
        pagina = 1
        while pagina is not None:
            payload_all_convenios = f'?codigoIBGE={entidade.codigo_municipio}&pagina={pagina}'
            sucess = True
            while sucess:
                try:
                    res = requests.get(url_base + '/convenios' + payload_all_convenios, headers=headers)
                    if res.json():
                        # print('passou')
                        # print(entidade)
                        # pagina += 1
                        res = json.loads(res.content)
                        tipo_orgao, created = TipoOrgao.objects.get_or_create(descricao='Outros')
                        posicaoDoArray = 0
                        while posicaoDoArray == len(res):
                            interveniente, created = Orgao.objects.get_or_create(
                                tipo=tipo_orgao,
                                nome=res[posicaoDoArray]['unidadeGestora']['nome'],
                                defaults={
                                    'tipo': tipo_orgao,
                                    'nome': res[posicaoDoArray]['unidadeGestora']['nome']
                                }
                            )
                            concedente, created = Orgao.objects.get_or_create(
                                tipo=tipo_orgao,
                                nome=res[posicaoDoArray]['unidadeGestora']['orgaoVinculado']['nomeOriginal'],
                                defaults={
                                    'tipo': tipo_orgao,
                                    'nome': res[posicaoDoArray]['unidadeGestora']['orgaoVinculado']['nomeOriginal']
                                }
                            )
                            dataInicio = datetime.strptime(res[posicaoDoArray]['dataInicioVigencia'], '%d/%m/%Y')
                            dateFinal = datetime.strptime(res[posicaoDoArray]["dataFinalVigencia"], '%d/%m/%Y')
                            ano = res[posicaoDoArray]["dataFinalVigencia"].split('/')[2]
                            inst, created = Instrumento.objects.get_or_create(
                                numero_operacao=res[posicaoDoArray]['convenio']['numeroOriginal'],
                                defaults={
                                    'entidade': entidade,
                                    'tipo':
                                        TipoInstrumento.objects.get_or_create(
                                            descricao=res[1]['tipoInstrumento']['descricao'],
                                            defaults={'descricao': res[posicaoDoArray][
                                                'tipoInstrumento']['descricao']})[0],
                                    'numero_operacao': res[posicaoDoArray]['convenio']['numeroOriginal'],
                                    'siafi_sicony': res[posicaoDoArray]['convenio']['numero'],
                                    'concedente': concedente,
                                    'interveniente': interveniente,
                                    'inicio': dataInicio,
                                    'termino': dateFinal,
                                    'ano': int(ano),
                                    'prorrogado': dateFinal,
                                    'repasse': res[posicaoDoArray]['valor'],
                                    'contrapartida': res[posicaoDoArray]['valorContrapartida'],
                                    'total': res[posicaoDoArray]['valor'] + res[posicaoDoArray]['valorContrapartida'],
                                    'objeto': res[posicaoDoArray]['convenio']['objeto']
                                }
                            )
                    else:
                        print('vazio')
                        pagina = None
                except ConnectionError:
                    sleep(10)

    instrument = Instrumento.objects.all()
    return render(request,'instrumento/instrumento.html', {'entidades': instrument})

    #return JsonResponse(get_entidade, safe=False)


