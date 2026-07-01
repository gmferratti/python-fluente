"""
Sintaxe moderna de criação e manipulação de dicts (3.1).

Dictcomps seguem a mesma lógica de listcomps. `**` desempacota mapeamentos em
chamadas de função e literais; dentro de um literal `dict`, chaves duplicadas
são permitidas e a última ocorrência prevalece. `|`/`|=` fazem para dicts o
que `+`/`+=` fazem para listas: um cria um objeto novo, o outro modifica no
lugar.
"""

DIAL_CODES = [
    (880, "Bangladesh"), (55, "Brazil"), (86, "China"),
    (91, "India"), (62, "Indonesia"), (81, "Japan"),
]


def dictcomp_pais_para_codigo():
    """A dictcomp inverte (código, país) para {país: código}."""
    return {country: code for code, country in DIAL_CODES}


def dictcomp_com_filtro():
    """Filtro e transformação numa dictcomp, igual a uma listcomp."""
    country_dial = dictcomp_pais_para_codigo()
    return {
        code: country.upper()
        for country, code in sorted(country_dial.items())
        if code < 70
    }


def star_star_em_chamada_de_funcao():
    """`**` pode aparecer mais de uma vez numa chamada, sem chaves repetidas."""
    def dump(**kwargs):
        return kwargs

    return dump(**{"x": 1}, y=2, **{"z": 3})


def star_star_em_literal_dict():
    """Em literal `dict`, chaves duplicadas são permitidas: a última vence."""
    return {"a": 0, **{"x": 1}, "y": 2, **{"z": 3, "x": 4}}


def merge_com_pipe():
    """`|` cria um dict novo; `|=` modifica no lugar (paralelo a `+`/`+=`)."""
    d1 = {"a": 1, "b": 3}
    d2 = {"a": 2, "b": 4, "c": 6}

    novo = d1 | d2
    d1_inalterado = dict(d1)

    d1 |= d2
    return novo, d1_inalterado, d1
