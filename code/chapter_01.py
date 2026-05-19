import collections
import math
from random import choice, shuffle

# ---------------------------------------------------------------------------
# Tipos
# ---------------------------------------------------------------------------

Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    """Baralho frances de 52 cartas.

    Demonstra como __len__ e __getitem__ integram uma classe customizada
    ao modelo de dados do Python, habilitando len(), indexacao, slicing,
    iteracao, reversed() e o operador 'in' sem heranca de nenhum tipo builtin.

    __setitem__ e necessario para que random.shuffle() funcione, pois ele
    troca elementos por posicao (deck[i] = deck[j]).
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


class Vector:
    """Vetor 2D.

    Demonstra metodos especiais aritmeticos e de representacao.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        # __repr__ e preferido a __str__ porque aparece no console interativo,
        # dentro de colecoes e em mensagens de erro — contextos onde o
        # desenvolvedor precisa de informacao precisa, nao de texto bonito.
        # O !r aplica repr() aos valores, garantindo que strings apareçam
        # com aspas e tipos especiais sejam identificaveis.
        return f"Vector({self.x!r}, {self.y!r})"

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        # False apenas para o vetor nulo; qualquer outro vetor e True
        return bool(abs(self))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


# ---------------------------------------------------------------------------
# Funcao de ordenacao para FrenchDeck
# ---------------------------------------------------------------------------

# Peso de cada naipe na convencao "spades high" (usada no bridge)
SUIT_VALUES = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    """Chave de ordenacao que posiciona as cartas de 2 de clubs (menor)
    ate As de spades (maior).

    Formula: rank_value * 4 + suit_value

    Multiplicar por 4 (numero de naipes) garante que qualquer carta de rank
    superior supere todas as de rank inferior, independente do naipe:
        2 de clubs  -> 0  * 4 + 0 = 0
        2 de spades -> 0  * 4 + 3 = 3
        3 de clubs  -> 1  * 4 + 0 = 4   (maior que qualquer "2")
        As de spades-> 12 * 4 + 3 = 51
    """
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(SUIT_VALUES) + SUIT_VALUES[card.suit]


# ---------------------------------------------------------------------------
# Demonstracoes
# ---------------------------------------------------------------------------

def demo_french_deck():
    deck = FrenchDeck()

    print("=== __len__ ===")
    print(len(deck))

    print("\n=== __getitem__: indice simples e negativo ===")
    print(deck[0], deck[-1])

    print("\n=== __getitem__: slicing ===")
    print(deck[:3])

    print("\n=== choice() — funciona via __len__ + __getitem__ ===")
    print(choice(deck))

    print("\n=== iteracao direta (primeiras 5) ===")
    for card in deck[:5]:
        print(card)

    print("\n=== reversed() (primeiras 5 do reverso) ===")
    for card in list(reversed(deck))[:5]:
        print(card)

    print("\n=== operador 'in' ===")
    print(Card("Q", "hearts") in deck)  # True
    print(Card("Q", "beasts") in deck)  # False

    print("\n=== shuffle() — requer __setitem__ (primeiras 5 apos shuffle) ===")
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
    print(bool(v1))           # True: vetor nao nulo
    print(bool(Vector(0, 0))) # False: vetor nulo


if __name__ == "__main__":
    demo_french_deck()
    demo_vector()
