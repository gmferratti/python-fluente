"""
Views de dicionário (3.7).

`.keys()`, `.values()` e `.items()` devolvem views, projeções somente
leitura sobre a estrutura interna do dict, não cópias. Uma view acompanha o
dicionário original em tempo real, sem precisar ser recriada a cada consulta.
"""


def view_reflete_mudanca_no_dict_original():
    """A view criada antes de um novo item ainda mostra o item depois."""
    d = dict(a=10, b=20, c=30)
    values = d.values()

    antes = list(values)
    d["z"] = 99
    depois = list(values)  # já inclui o 99, sem recriar a view

    return antes, depois


def view_nao_e_indexavel():
    """Views não suportam indexação por posição."""
    d = dict(a=10, b=20)
    try:
        d.values()[0]
    except TypeError as exc:
        return repr(exc)
    raise AssertionError("esperava TypeError")
