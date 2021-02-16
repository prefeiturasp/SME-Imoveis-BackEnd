import logging

from requests.exceptions import HTTPError

from sme_ofertaimoveis.dados_comuns.utils import TerceirizadasClient
from sme_ofertaimoveis.dados_comuns.models import DiretoriaRegional, Distrito, Setor, Subprefeitura

log  = logging.getLogger(__name__)


def atualiza_dados_comuns():
    try:
        log.debug("Consultando dres.")
        dres = TerceirizadasClient.dres()
        atualiza_dados_dres(dres)
        log.info("Total dres %s.", len(dres))

        log.info("Consultando sub-prefeituras.")        
        subprefeituras = TerceirizadasClient.subprefeituras()
        atualiza_dados_subprefeituras(subprefeituras)
        log.info("Total sub %s.", len(subprefeituras))

        log.info("Consultando distritos.")
        distritos = TerceirizadasClient.distritos()
        atualiza_dados_distritos(distritos)
        log.info("Total dis %s.", len(distritos))

        log.info("Consultando setores.")
        setores = TerceirizadasClient.setores()
        atualiza_dados_setores(setores)
        log.info("Total set %s.", len(setores))

        return "Dados atualizados com sucesso."
    except HTTPError as httperror:
        log.info("Erro ao atualizar dados. %s", str(httperror))
        return ("Erro ao atualizar dados. %s", str(httperror))


def atualiza_dados_dres(dres):
    """Se não existe é criado caso contrário seus dados são atualizados."""
    for dre_dict in dres:
        dre = DiretoriaRegional.objects.filter(codigo_eol=dre_dict['cod_dre'].strip()).first()
        
        # A sigla vem da API do eol como no exemplo: "DRE - MP"
        # então o trecho abaixo retorna apenas "MP" pra manter o padrão que já vinha
        # sendo utilizado
        sg = dre_dict['sg_dre'].split('-')[1].strip()
        # O nome da dre vem da API do eol como no exemplo:DIRETORIA REGIONAL DE EDUCACAO SAO MIGUEL
        # então o trecho de código abaixo retorna "SAO MIGUEL"
        # para manter o padrão que já vinha sendo utilizado.
        nm_dre = dre_dict['dre'].split('EDUCACAO')[1].strip()

        if not dre:
            log.info("Criando dre %s, %s", nm_dre, sg)
            DiretoriaRegional.objects.create(
                codigo_eol=dre_dict['cod_dre'].strip(),
                nome=nm_dre,
                sigla=sg
            )
        else:
            log.info("Atualizando dados da dre %s, %s", nm_dre, sg)
            dre.nome = nm_dre
            dre.sigla = sg
            dre.save()


def atualiza_dados_subprefeituras(subprefeituras):
    """Criar subprefeituras caso não exista na base."""
    for sub_dict in subprefeituras:
        subprefeitura = Subprefeitura.objects.filter(nome=sub_dict['dc_sub_prefeitura'].strip()).first()

        if not subprefeitura:
            log.info("Criando dados da subprefeitura %s", sub_dict['dc_sub_prefeitura'].strip())
            dres = DiretoriaRegional.objects.filter(codigo_eol=dre_dict['cod_dre'].strip()).all()
            sub = Subprefeitura.objects.create(
                nome=sub_dict['dc_sub_prefeitura'].strip()
            )

            sub.dre.add(*dres)
    
    
def atualiza_dados_distritos(distritos):
    """Tentativa de atualizar os dados de um distrito pelo nome.
    A única informação relavante retornada pela API do eol é nome do distrito."""
    for distrito_dict in distritos:
        distrito = Distrito.objects.filter(nome__icontains=distrito_dict['nm_distrito_mec'].strip()).first()
        
        if distrito:
            log.info("Atualizando dados do distrito %s.", distrito_dict['nm_distrito_mec'].strip())
            distrito.nome = distrito_dict['nm_distrito_mec'].strip()
            distrito.save()


def atualiza_dados_setores(setores):
    """Tentativa de atualizar os dados de um setor."""
    for setor_dict in setores:
        setor = Setor.objects.filter(codigo=setor_dict['cd_setor_distrito']).first()
        
        if not setor:
            log.info("Criando dados do setor %s.", setor_dict['cd_setor_distrito'].strip())
            Setor.objects.create(
                codigo=setor_dict['cd_setor_distrito']
            )
