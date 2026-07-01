"""
Capítulo 02 — Uma Coleção de Sequências

Módulos (numerados na ordem em que aparecem nas notas):
    _01_comprehensions            →  listcomps, genexps (2.3)
    _02_tuplas                    →  tuplas como registro, memória, mutabilidade (2.4)
    _03_desempacotamento          →  *, **, aninhado, METRO_AREAS (2.5)
    _04_pattern_matching          →  match/case sobre sequências (2.6)
    _05_fatiamento                →  slice, INVOICE, atribuição em fatia (2.7)
    _06_operadores                →  +, *, +=, *= com sequências (2.8)
    _07_ordenacao                 →  list.sort() vs sorted() (2.9)
    _08_estruturas_especializadas →  array, memoryview, NumPy, deque (2.10)
    demo                          →  demonstrações executáveis
"""

from ._03_desempacotamento import METRO_AREAS
from ._05_fatiamento import DESCRIPTION, INVOICE, SKU, UNIT_PRICE

__all__ = ["METRO_AREAS", "INVOICE", "SKU", "DESCRIPTION", "UNIT_PRICE"]
