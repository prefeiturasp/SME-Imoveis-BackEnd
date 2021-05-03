from django.template.loader import render_to_string


def relatorio_cadastro(data: dict):
    html_string = render_to_string('imovel/relatorios/relatorio_cadastro.html', data)

    return html_string
