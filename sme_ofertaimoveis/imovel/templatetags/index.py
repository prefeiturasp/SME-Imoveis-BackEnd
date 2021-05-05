from django import template

register = template.Library()

# Retorna o valor de um atributo do elemento
@register.filter
def get_attribute(elemento, atributo):
    return elemento.get(atributo)
    # return getattr(elemento, atributo, False)

# Retorna o elemento da lista de acordo com o index
@register.filter
def get_element_by_index(indexable, i):
    return indexable[i]

# Verifica se o Log é do tipo cancelled
@register.filter
def fim_de_fluxo(logs):
    fim = False
    for log in logs:
        if ('neg' in log['status_evento_explicacao'] or 'não' in log['status_evento_explicacao'] or
            'cancel' in log['status_evento_explicacao']):  # noqa
            fim = True
    return fim

# Retorna classe css correta de acordo com o log
@register.filter  # noqa C901
def class_css(log):
    classe_css = 'pending'
    if log['status_evento_explicacao'] in ['SME analisou previamente', 'Enviado à COMAPRE', 'Agendamento da vistoria',
                                        'Aguardando relatório de vistoria', 'Aguardando laudo de valor locatício',
                                        'Relatório da vistoria', 'Laudo de valor locatício', 'Vistoria aprovada',
                                        'Enviado à DRE', 'Finalizado - Aprovado']:
        classe_css = 'active'
    elif log['status_evento_explicacao'] in ['Cancelado']:
        classe_css = 'cancelled'
    elif log['status_evento_explicacao'] in ['Finalizado - Área Insuficiente', 'Finalizado - Demanda Insuficiente', 'Finalizado - Não atende as necessidades da SME',
                                          'Finalizado - Reprovado', 'Vistoria reprovada']:
        classe_css = 'disapproved'
    elif log['status_evento_explicacao'] in []:
        classe_css = 'questioned'
    return classe_css

# Retorna true se o index for menor ou igual ao tamanho da lista de logs
@register.filter
def index_exists(indexable, i):
    return i <= len(indexable)

# Compara logs com fluxo da linha do tempo, retorna o maior
@register.filter
def or_logs(fluxo, logs):
    return logs if len(logs) > len(fluxo) else fluxo

# verifica se o fluxo usado é maior que a linha do tempo
@register.filter
def is_bigger_than_flow(logs, fluxo):
    return True if len(logs) > len(fluxo) else False
