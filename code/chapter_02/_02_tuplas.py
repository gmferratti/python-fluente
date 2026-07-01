"""
Tuplas como registro e como lista imutável (2.4).

A imutabilidade de uma tupla vale para as referências que ela guarda, não
para o conteúdo dos objetos referenciados. Por isso uma tupla com item
mutável pode ter esse item alterado, e por isso ela não é hashable.
"""

import sys


def tuplas_como_registros():
    """A posição de cada item carrega significado (latitude/longitude, CSV...)."""
    brasilia = (-15.7797, -47.9297)
    lat, lon = brasilia

    registro = ("São Paulo", 2024, 11_451_245)
    cidade, ano, pop = registro

    return f"{cidade} tinha {pop:,} hab. em {ano} (lat={lat}, lon={lon})"


def desempacotamento_posicional():
    """Swap, descarte com `_` e captura do restante com `*`."""
    a, b = 10, 20
    a, b = b, a  # a=20, b=10

    registro = ("São Paulo", 2024, 11_451_245)
    _, ano, _ = registro

    primeiro, *meio, ultimo = (1, 2, 3, 4, 5)

    return {"a": a, "b": b, "ano": ano, "primeiro": primeiro, "meio": meio, "ultimo": ultimo}


def memoria_tupla_vs_lista():
    """Tupla usa menos memória do que lista por não sofrer overallocation."""
    t = (1, 2, 3, 4, 5)
    l = [1, 2, 3, 4, 5]
    return sys.getsizeof(t), sys.getsizeof(l)


def tuplas_com_itens_mutaveis():
    """A imutabilidade é da referência, não do conteúdo referenciado."""
    t = ([1, 2], [3, 4])
    t[0].append(99)  # OK: mutamos a lista interna, não a tupla

    try:
        t[0] = [9, 9]  # TypeError: não podemos trocar a referência
    except TypeError as exc:
        return t, repr(exc)
    raise AssertionError("esperava TypeError")


def tupla_com_mutavel_nao_e_hashable():
    """Uma tupla só é hashable se todos os seus itens também forem."""
    t = ([1, 2], [3, 4])
    try:
        hash(t)
    except TypeError as exc:
        return repr(exc)
    raise AssertionError("esperava TypeError")
