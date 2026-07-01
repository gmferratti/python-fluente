"""
Capítulo 01 — O Modelo de Dados do Python

Módulos (numerados na ordem em que aparecem nas notas):
    _01_french_deck  →  Card, FrenchDeck, spades_high  (protocolo de sequência)
    _02_vector       →  Vector                          (operadores aritméticos)
    demo             →  demonstrações executáveis
"""

from ._01_french_deck import Card, FrenchDeck, spades_high
from ._02_vector import Vector

__all__ = ["Card", "FrenchDeck", "spades_high", "Vector"]
