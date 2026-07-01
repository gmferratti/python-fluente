"""
Protocolo de sequência via métodos especiais.

Implementar apenas __len__ e __getitem__ é suficiente para que Python trate
FrenchDeck como uma sequência completa: len(), indexação, slicing, iteração,
reversed() e o operador 'in' funcionam sem herança de nenhum tipo built-in.
__setitem__ é acrescentado para habilitar random.shuffle(), que troca
elementos por posição.
"""

import collections
from random import choice, shuffle


Card = collections.namedtuple("Card", ["rank", "suit"])

# Peso de cada naipe na convenção "spades high" (usada no bridge)
SUIT_VALUES = dict(spades=3, hearts=2, diamonds=1, clubs=0)


class FrenchDeck:
    """Baralho francês de 52 cartas.

    Demonstra como __len__ e __getitem__ integram uma classe customizada
    ao modelo de dados do Python, habilitando len(), indexação, slicing,
    iteração, reversed() e o operador 'in' sem herança de nenhum tipo built-in.

    __setitem__ é necessário para que random.shuffle() funcione, pois ele
    troca elementos por posição (deck[i] = deck[j]).
    """

    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):
        self._cards[position] = value


def spades_high(card: Card) -> int:
    """Chave de ordenação: posiciona as cartas de 2♣ (menor) até A♠ (maior).

    Fórmula: rank_value * 4 + suit_value

    Multiplicar por 4 (número de naipes) garante que qualquer carta de rank
    superior supere todas as de rank inferior, independentemente do naipe:
        2♣ →  0 * 4 + 0 =  0
        2♠ →  0 * 4 + 3 =  3
        3♣ →  1 * 4 + 0 =  4   (maior que qualquer "2")
        A♠ → 12 * 4 + 3 = 51
    """
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(SUIT_VALUES) + SUIT_VALUES[card.suit]
