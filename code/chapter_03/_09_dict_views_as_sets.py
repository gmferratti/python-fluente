"""
Operações de conjunto em views de dict (3.10).

`dict_keys` e `dict_items` implementam boa parte da API de `frozenset`, o
que permite comparar chaves (ou itens) de dois dicts sem converter para
`set` explicitamente.
"""


def chaves_em_comum_entre_dois_dicts():
    """`d1.keys() & d2.keys()` funciona sem conversão explícita para set."""
    d1 = dict(a=1, b=2, c=3, d=4)
    d2 = dict(b=20, d=40, e=50)
    return d1.keys() & d2.keys()


def chaves_em_comum_com_set_comum():
    """A mesma view também combina com um `set` comum."""
    d1 = dict(a=1, b=2, c=3, d=4)
    s = {"a", "e", "i"}
    return d1.keys() & s
