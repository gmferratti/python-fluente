"""
Métodos especiais aritméticos e de representação.

Vector mostra como __repr__, __abs__, __bool__, __add__ e __mul__ integram
um tipo customizado aos operadores e funções built-in do Python.
"""

import math


class Vector:
    """Vetor 2D com suporte a operações aritméticas básicas."""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        # __repr__ é preferido a __str__ porque aparece no console interativo,
        # dentro de coleções e em mensagens de erro — contextos onde o
        # desenvolvedor precisa de informação precisa, não de texto bonito.
        # O !r aplica repr() aos valores, garantindo que strings apareçam
        # com aspas e tipos especiais sejam identificáveis.
        return f"Vector({self.x!r}, {self.y!r})"

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        # False apenas para o vetor nulo; qualquer outro vetor é True
        return bool(abs(self))

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)
