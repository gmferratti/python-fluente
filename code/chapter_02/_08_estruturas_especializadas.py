"""
Alternativas à `list` (2.10): array, memoryview, NumPy, deque.

`array.array` é uma sequência plana (guarda valores crus, sem indireção de
objetos). `memoryview` compartilha a memória de outra estrutura sem copiar.
NumPy troca laços `for` por operações vetorizadas em código C. `deque` troca
o array dinâmico contíguo da `list` por blocos encadeados, tornando
inserção/remoção nas duas pontas O(1).
"""

import array
from collections import deque
from random import random


def array_de_floats(n=10**6):
    """`array.array` guarda valores crus, sem indireção de objetos Python."""
    return array.array("d", (random() for _ in range(n)))


def array_grava_e_le_em_disco(caminho, n=10**6):
    """Gravar/ler um array é cópia direta de bytes, sem parsing linha a linha."""
    floats = array_de_floats(n)

    with open(caminho, "wb") as fp:
        floats.tofile(fp)

    floats2 = array.array("d")
    with open(caminho, "rb") as fp:
        floats2.fromfile(fp, n)

    return floats2 == floats


def memoryview_sobre_array():
    """`memoryview` enxerga os bytes de outra estrutura sem copiar."""
    numeros = array.array("h", [-2, -1, 0, 1, 2])  # 'h' = short int
    memv = memoryview(numeros)

    memv_oct = memv.cast("B")  # reinterpreta como bytes crus
    antes = memv_oct.tolist()

    memv_oct[5] = 4  # altera a view -> altera o array original
    return antes, numeros


def numpy_soma_vetorizada():
    """Somar dois vetores elemento a elemento, sem laço `for`."""
    import numpy as np

    a = np.array([1, 2, 3, 4, 5])
    b = np.array([10, 20, 30, 40, 50])
    return a + b


def numpy_quadrado_vetorizado():
    """Elevar cada item ao quadrado com uma operação vetorizada."""
    import numpy as np

    numeros = np.arange(10)
    return numeros ** 2


def numpy_filtro_com_mascara():
    """Indexação booleana equivale ao `if` de uma comprehension."""
    import numpy as np

    numeros = np.arange(20)
    mascara = (numeros > 10) & (numeros % 2 == 0)
    return numeros[mascara]


def numpy_distancia_euclidiana():
    """Fatiamento multidimensional (`a[:, 0]`) + operação vetorizada."""
    import numpy as np

    pontos = np.array([(1, 2), (3, 4), (5, 6)])
    x, y = pontos[:, 0], pontos[:, 1]
    return np.sqrt(x**2 + y**2)


def deque_rotate():
    """`rotate(n)` é O(1) por operar só nas pontas, sem mover o meio."""
    dq = deque(range(10), maxlen=10)
    dq.rotate(3)
    girada_direita = list(dq)
    dq.rotate(-4)
    girada_esquerda = list(dq)
    return girada_direita, girada_esquerda


def deque_buffer_circular():
    """`maxlen` transforma a deque num buffer circular automático."""
    dq = deque([10, 20, 30], maxlen=3)
    dq.appendleft(0)   # empurra o 30 para fora
    depois_appendleft = list(dq)
    dq.append(99)
    depois_append = list(dq)
    return depois_appendleft, depois_append
