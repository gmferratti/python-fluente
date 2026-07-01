"""
Desempacotamento de coleções (2.5).

`*` absorve o que sobra numa atribuição e sempre devolve uma lista, mesmo
vindo de uma tupla ou de outro iterável. A PEP 448 estende esse mesmo `*`
(e o `**` para mapeamentos) para chamadas de função e literais.
"""

import os

METRO_AREAS = [
    ("Tokyo", "JP", 36.933, (35.689722, 139.691667)),
    ("São Paulo", "BR", 19.649, (-23.547778, -46.635833)),
]


def unpacking_path_split():
    """`*` combinado com métodos de string/path para pegar extremidades."""
    _, filename = os.path.split("/home/user/docs/report.pdf")
    *_, last = "/usr/local/bin/python".split("/")
    return filename, last


def star_recolhe_excesso():
    """`*` sempre devolve uma lista, mesmo vindo de um `range` ou tupla."""
    primeiro, *resto = range(5)
    *inicio, ultimo = range(5)
    primeiro2, *meio, ultimo2 = range(6)
    a, b, *_ = (10, 20, 30, 40, 50)

    return {
        "primeiro": primeiro, "resto": resto,
        "inicio": inicio, "ultimo": ultimo,
        "meio": meio, "a": a, "b": b,
    }


def star_em_chamadas_e_literais():
    """PEP 448: `*`/`**` em chamadas de função e literais de coleção."""
    def soma(a, b, c):
        return a + b + c

    args = (1, 2, 3)
    resultado_chamada = soma(*args)

    l1, l2 = [1, 2, 3], [4, 5]
    merged = [*l1, *l2, 6]

    d1, d2 = {"a": 1}, {"b": 2}
    merged_dict = {**d1, **d2, "c": 3}

    return resultado_chamada, merged, merged_dict


def desempacotamento_aninhado():
    """Extrai o primeiro resultado de uma "query" com múltiplas colunas."""
    query_result = [("Tokyo", "JP", 37_400_000)]
    [(city, _, pop)] = query_result

    hemisferio_oeste = []
    for name, _, _, (lat, lon) in METRO_AREAS:
        if lon <= 0:
            hemisferio_oeste.append(f"{name}: {lat:.4f}N, {lon:.4f}W")

    return f"{city}: {pop:,}", hemisferio_oeste
