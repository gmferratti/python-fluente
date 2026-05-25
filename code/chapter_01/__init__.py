"""
Capítulo 01 — O Modelo de Dados do Python

Módulos:
    french_deck  →  Card, FrenchDeck, spades_high  (protocolo de sequência)
    vector       →  Vector                          (operadores aritméticos)
    demo         →  demonstrações executáveis
"""

from .french_deck import Card, FrenchDeck, spades_high
from .vector import Vector

__all__ = ["Card", "FrenchDeck", "spades_high", "Vector"]
