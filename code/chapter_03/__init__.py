"""
Capítulo 03 — Dicionários e Conjuntos

Módulos (numerados na ordem em que aparecem nas notas):
    _01_dict_comprehensions →  dictcomp, ** e | / |= (3.1)
    _02_pattern_matching    →  match/case sobre mapeamentos (3.2)
    _03_setdefault          →  hashabilidade, setdefault (3.3)
    _04_missing_and_defaultdict →  defaultdict, __missing__, StrKeyDict0 (3.4)
    _05_dict_variants       →  ChainMap, Counter, StrKeyDict via UserDict (3.5)
    _06_immutable_mappings  →  types.MappingProxyType (3.6)
    _07_dict_views          →  .keys()/.values()/.items() como views (3.7)
    _08_sets                →  set, frozenset, álgebra de conjuntos (3.9)
    _09_dict_views_as_sets  →  dict_keys/dict_items como conjuntos (3.10)
    demo                    →  demonstrações executáveis

A seção 3.8 (consequências da tabela de hash) é só conceitual, sem exemplo
executável correspondente.
"""

from ._04_missing_and_defaultdict import StrKeyDict0
from ._05_dict_variants import StrKeyDict

__all__ = ["StrKeyDict0", "StrKeyDict"]
