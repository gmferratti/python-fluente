"""
Demonstrações executáveis do capítulo 01.

Execute diretamente:
    python -m chapter_01.demo
"""

from random import choice, shuffle

from ._01_french_deck import Card, FrenchDeck, spades_high
from ._02_vector import Vector


def demo_french_deck():
    deck = FrenchDeck()

    print("=== __len__ ===")
    print(len(deck))

    print("\n=== __getitem__: índice simples e negativo ===")
    print(deck[0], deck[-1])

    print("\n=== __getitem__: slicing ===")
    print(deck[:3])

    print("\n=== choice() — funciona via __len__ + __getitem__ ===")
    print(choice(deck))

    print("\n=== iteração direta (primeiras 5) ===")
    for card in deck[:5]:
        print(card)

    print("\n=== reversed() (primeiras 5 do reverso) ===")
    for card in list(reversed(deck))[:5]:
        print(card)

    print("\n=== operador 'in' ===")
    print(Card("Q", "hearts") in deck)   # True
    print(Card("Q", "beasts") in deck)   # False

    print("\n=== shuffle() — requer __setitem__ (primeiras 5 após shuffle) ===")
    shuffle(deck)
    for card in deck[:5]:
        print(card)

    print("\n=== sorted() com spades_high (5 cartas mais altas) ===")
    for card in sorted(deck, key=spades_high)[-5:]:
        print(card)


def demo_vector():
    v1 = Vector(2, 4)
    v2 = Vector(2, 1)

    print("\n=== __repr__ ===")
    print(repr(v1))

    print("\n=== __add__ ===")
    print(v1 + v2)

    print("\n=== __mul__ ===")
    print(v1 * 3)

    print("\n=== __abs__ ===")
    print(abs(v1))

    print("\n=== __bool__ ===")
    print(bool(v1))             # True: vetor não nulo
    print(bool(Vector(0, 0)))   # False: vetor nulo


if __name__ == "__main__":
    demo_french_deck()
    demo_vector()
