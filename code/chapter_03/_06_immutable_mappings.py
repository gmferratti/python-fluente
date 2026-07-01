"""
Mapeamentos imutáveis (3.6).

`types.MappingProxyType` cria uma visão somente leitura e dinâmica sobre um
dict existente: o proxy não pode ser modificado diretamente, mas reflete
qualquer mudança feita no dict original.
"""

from types import MappingProxyType


def mappingproxy_e_somente_leitura_mas_dinamico():
    """Escrever no proxy falha; escrever no dict original aparece no proxy."""
    d = {1: "A"}
    d_proxy = MappingProxyType(d)

    valor_lido = d_proxy[1]

    try:
        d_proxy[2] = "x"
    except TypeError as exc:
        erro = repr(exc)
    else:
        raise AssertionError("esperava TypeError")

    d[2] = "B"  # muda o dict original, não o proxy
    return valor_lido, erro, dict(d_proxy)
