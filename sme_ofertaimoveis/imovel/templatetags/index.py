from django import template


register = template.Library()

@register.filter
def get_attribute(elemento, atributo):
    return getattr(elemento, atributo, False)


@register.filter
def get_element_by_index(indexable, i):
    return indexable[i]


@register.filter
def index_exists(indexable, i):
    return i <= len(indexable)


@register.filter
def fim_de_fluxo(logs):
    fim = False
    for log in logs:
        if ('neg' in log.status_evento_explicacao or 'não' in log.status_evento_explicacao or
            'cancel' in log.status_evento_explicacao):  # noqa
            fim = True
    return fim


@register.filter  # noqa C901
def class_css(log):
    classe_css = 'pending'
    if log.status_evento_explicacao in ['Solicitação Realizada', 'Escola revisou', 'DRE validou', 'DRE revisou',
                                        'CODAE autorizou', 'Terceirizada tomou ciência', 'Escola solicitou inativação',
                                        'CODAE autorizou inativação', 'Terceirizada tomou ciência da inativação',
                                        'CODAE homologou', 'CODAE autorizou reclamação']:
        classe_css = 'active'
    elif log.status_evento_explicacao in ['Escola cancelou', 'DRE cancelou', 'Terceirizada cancelou homologação',
                                          'CODAE suspendeu o produto']:
        classe_css = 'cancelled'
    elif log.status_evento_explicacao in ['DRE não validou', 'CODAE negou', 'Terceirizada recusou',
                                          'CODAE negou inativação', 'CODAE não homologou']:
        classe_css = 'disapproved'
    elif log.status_evento_explicacao in ['Questionamento pela CODAE', 'CODAE pediu correção',
                                          'CODAE pediu análise sensorial', 'Escola/Nutricionista reclamou do produto',
                                          'CODAE pediu análise da reclamação']:
        classe_css = 'questioned'
    return classe_css


@register.filter
def index_exists(indexable, i):
    return i <= len(indexable)


@register.filter
def or_logs(fluxo, logs):
    return logs if len(logs) > len(fluxo) else fluxo