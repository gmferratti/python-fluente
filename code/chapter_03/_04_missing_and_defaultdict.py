"""
Tratamento automático de chaves ausentes (3.4).

`defaultdict` chama `default_factory` sempre que `d[k]` não encontra a
chave. `__missing__` é o mecanismo mais geral por trás disso: qualquer
subclasse de `dict` pode implementá-lo para customizar o que acontece numa
busca que falharia com `KeyError`.
"""

import collections


def indice_com_defaultdict(pares):
    """`defaultdict(list)` cria a lista vazia automaticamente em `d[k]`."""
    index = collections.defaultdict(list)
    for word, location in pares:
        index[word].append(location)
    return index


class StrKeyDict0(dict):
    """Trata chaves numéricas e string como equivalentes, via `__missing__`.

    O `isinstance(key, str)` no início evita recursão infinita: se a chave
    já é string e ainda assim não foi encontrada, não há mais nada a
    converter, então o método desiste com KeyError.
    """

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()


def str_key_dict0_aceita_chave_numerica_ou_string():
    """`d['2']` e `d[2]` são equivalentes, mesmo criando o dict só com strings."""
    d = StrKeyDict0([("2", "two"), ("4", "four")])
    return d["2"], d[2], d.get("4"), d.get(1, "N/A"), 2 in d, 1 in d
