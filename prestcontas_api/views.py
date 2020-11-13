import json
from datetime import datetime
from time import sleep

from django.shortcuts import render
import requests
from prestcontas_api.models import Entidade, Instrumento, TipoInstrumento, TipoOrgao, Orgao


def index(request):
    entidades = Entidade.objects.all()
    headers = {'chave-api-dados': '99d565aeacc2e7414dadd7a377f17417', 'Accept': "*/*"}
    url_base = 'http://www.portaltransparencia.gov.br/api-de-dados'

    for entidade in entidades:
        pagina = 1
        while pagina is not None:
            payload_all_convenios = f'?codigoIBGE={entidade.codigo_municipio}&pagina={pagina}'
            success = True
            while success:
                try:
                    res = requests.get(url_base + '/convenios' + payload_all_convenios, headers=headers)
                    if res.json():
                        res = json.loads(res.content)
                        tipo_orgao, created = TipoOrgao.objects.get_or_create(descricao='Outros')
                        posicao_do_array = 0
                        while posicao_do_array == len(res):
                            interveniente, created = Orgao.objects.get_or_create(
                                tipo=tipo_orgao,
                                nome=res[posicao_do_array]['unidadeGestora']['nome'],
                                defaults={
                                    'tipo': tipo_orgao,
                                    'nome': res[posicao_do_array]['unidadeGestora']['nome']
                                }
                            )
                            concedente, created = Orgao.objects.get_or_create(
                                tipo=tipo_orgao,
                                nome=res[posicao_do_array]['unidadeGestora']['orgaoVinculado']['nomeOriginal'],
                                defaults={
                                    'tipo': tipo_orgao,
                                    'nome': res[posicao_do_array]['unidadeGestora']['orgaoVinculado']['nomeOriginal']
                                }
                            )
                            data_inicio = datetime.strptime(res[posicao_do_array]['dataInicioVigencia'], '%d/%m/%Y')
                            data_final = datetime.strptime(res[posicao_do_array]["dataFinalVigencia"], '%d/%m/%Y')
                            ano = res[posicao_do_array]["dataFinalVigencia"].split('/')[2]
                            inst, created = Instrumento.objects.get_or_create(
                                numero_operacao=res[posicao_do_array]['convenio']['numeroOriginal'],
                                defaults={
                                    'entidade': entidade,
                                    'tipo':
                                        TipoInstrumento.objects.get_or_create(
                                            descricao=res[1]['tipoInstrumento']['descricao'],
                                            defaults={'descricao': res[posicao_do_array][
                                                'tipoInstrumento']['descricao']}
                                        )[0],
                                    'numero_operacao': res[posicao_do_array]['convenio']['numeroOriginal'],
                                    'siafi_sicony': res[posicao_do_array]['convenio']['numero'],
                                    'concedente': concedente,
                                    'interveniente': interveniente,
                                    'inicio': data_inicio,
                                    'termino': data_final,
                                    'ano': int(ano),
                                    'prorrogado': data_final,
                                    'repasse': res[posicao_do_array]['valor'],
                                    'contrapartida': res[posicao_do_array]['valorContrapartida'],
                                    'total': res[posicao_do_array]['valor'] + res[posicao_do_array]['valorContrapartida'],
                                    'objeto': res[posicao_do_array]['convenio']['objeto']
                                }
                            )
                            pagina += 1
                    else:
                        print('vazio')
                        pagina = None
                except ConnectionError:
                    sleep(10)

    instrument = Instrumento.objects.all()
    return render(request, 'instrumento/instrumento.html', {'entidades': instrument})
