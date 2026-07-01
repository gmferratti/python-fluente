"""
Variações de dict na biblioteca padrão (3.5).

`ChainMap` consulta vários mapeamentos como se fossem um só, escrevendo
sempre no primeiro. `Counter` é um dict especializado em contagem. `UserDict`
é a base recomendada para mapeamentos customizados: por composição (um dict
interno em `.data`), evita os atalhos internos em C que `dict` usa e que
ignoram métodos sobrescritos por uma subclasse direta.
"""

import collections
from collections import ChainMap


def chainmap_busca_em_cascata():
    """ChainMap busca na ordem dos mapeamentos e escreve só no primeiro."""
    d1 = dict(a=1, b=3)
    d2 = dict(a=2, b=4, c=6)
    chain = ChainMap(d1, d2)

    encontrado_em_d1 = chain["a"]      # 1, está em d1
    encontrado_em_d2 = chain["c"]      # 6, só está em d2

    chain["a"] = 100                   # escreve em d1, não em d2
    return encontrado_em_d1, encontrado_em_d2, d1, d2


def counter_contagem_e_most_common():
    """Counter suporta `+`, `-` e `most_common(n)`."""
    ct = collections.Counter("abracadabra")
    ct.update("aaaaazzz")
    return ct.most_common(3)


class StrKeyDict(collections.UserDict):
    """Mesma ideia de StrKeyDict0, mas via UserDict: mais curta e mais correta.

    Como UserDict estende MutableMapping, update() e get() já delegam
    corretamente para __setitem__/__getitem__, então toda chave inserida
    (na criação ou num update) é convertida para string.
    """

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item


def str_key_dict_converte_chaves_no_update():
    """Diferente de StrKeyDict0, update() também converte as chaves para string."""
    d = StrKeyDict([("2", "two")])
    d.update({4: "four"})
    return dict(d.data), 4 in d, "4" in d
