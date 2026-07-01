"""
Hashabilidade e `setdefault` (3.3).

Toda chave de dict precisa ser hashable. `setdefault` resolve em uma única
busca o padrão "pegue o valor da chave, criando-o com um default se ainda
não existir, e atualize-o".
"""


def exemplos_de_hashabilidade():
    """Tupla é hashable só se todo o conteúdo interno também for."""
    tt = (1, 2, (30, 40))              # hashable
    tf = (1, 2, frozenset([30, 40]))   # hashable: frozenset é hashable

    try:
        hash((1, 2, [30, 40]))         # não hashable: contém uma lista
    except TypeError as exc:
        return hash(tt), hash(tf), repr(exc)
    raise AssertionError("esperava TypeError")


def indice_com_get_e_atualizacao(pares):
    """Forma direta: até três buscas pela mesma chave (get + append + set)."""
    index = {}
    for word, location in pares:
        occurrences = index.get(word, [])
        occurrences.append(location)
        index[word] = occurrences
    return index


def indice_com_setdefault(pares):
    """`setdefault` faz o mesmo em uma única busca por chave."""
    index = {}
    for word, location in pares:
        index.setdefault(word, []).append(location)
    return index
