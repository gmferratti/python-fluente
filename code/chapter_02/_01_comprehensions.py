"""
Listcomps e genexps (2.3).

Listcomps substituem map()+filter() com uma sintaxe mais direta. Genexps usam
a mesma sintaxe, mas com () no lugar de []: implementam o protocolo de
iterador e nunca constroem a lista intermediária inteira em memória.
"""

from array import array

SYMBOLS = "café"


def listcomp_vs_map_filter():
    """Listcomp é mais legível do que combinar map + filter."""
    com_map_filter = list(filter(lambda c: ord(c) > 127, map(str.upper, SYMBOLS)))
    com_listcomp = [str.upper(c) for c in SYMBOLS if ord(c) > 127]

    assert com_map_filter == com_listcomp
    return com_listcomp


def walrus_em_listcomp():
    """O operador morsa (:=) evita recalcular ord(c) duas vezes por item."""
    sem_walrus = [ord(c) for c in SYMBOLS if ord(c) > 127]
    com_walrus = [code for c in SYMBOLS if (code := ord(c)) > 127]

    assert sem_walrus == com_walrus
    return com_walrus


def produto_cartesiano_listcomp():
    """Dois `for` numa listcomp geram o produto cartesiano entre duas sequências."""
    cores = ["preto", "branco"]
    tamanhos = ["S", "M", "L"]
    return [(cor, tam) for cor in cores for tam in tamanhos]


def genexp_construcao_array():
    """Genexp evita construir a lista intermediária inteira antes do array."""
    return array("I", (ord(c) for c in SYMBOLS))


def produto_cartesiano_genexp():
    """Genexp é ideal quando o resultado só será iterado uma vez."""
    cores = ["preto", "branco"]
    tamanhos = ["S", "M", "L"]
    return (f"{cor} {tam}" for cor in cores for tam in tamanhos)
