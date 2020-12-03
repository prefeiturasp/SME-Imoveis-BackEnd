def checa_digito_verificador_iptu(numero_iptu):
    multiplicacoes = [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    soma = 0
    indice = 0
    for digito in [char for char in numero_iptu[:-1] if char.isdigit()]:
        soma += int(digito) * multiplicacoes[indice]
        indice += 1
    mod = soma % 11 if soma % 11 != 10 else 1
    return int(numero_iptu[-1]) == mod
