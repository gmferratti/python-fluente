"""
`list.sort()` vs `sorted()` (2.9).

`sort()` ordena no próprio lugar e devolve None; `sorted()` devolve uma lista
nova e aceita qualquer iterável. Timsort (o algoritmo usado) é estável: itens
empatados no critério de comparação preservam a ordem relativa original.
"""


def sort_devolve_none():
    """`list.sort()` ordena no lugar e devolve None: não reatribua o resultado."""
    frutas = ["morango", "abacaxi", "banana"]
    valor_de_retorno = frutas.sort()
    return frutas, valor_de_retorno


def sorted_com_reverse_e_key():
    """`reverse` inverte o critério; `key` transforma o valor antes de comparar."""
    numeros = [5, 1, 4, 2, 3]
    decrescente = sorted(numeros, reverse=True)

    palavras = ["banana", "Abacaxi", "uva", "Kiwi"]
    por_minusculas = sorted(palavras, key=str.lower)
    por_tamanho = sorted(palavras, key=len)

    return decrescente, por_minusculas, por_tamanho


def sorted_e_estavel():
    """Timsort é estável: empates preservam a ordem relativa original."""
    alunos = [
        ("Ana", 8.5),
        ("Bruno", 7.0),
        ("Carla", 8.5),
        ("Davi", 7.0),
    ]
    por_nota = sorted(alunos, key=lambda a: a[1])

    # Ordenação em etapas: nome (secundário) depois nota (principal). Em caso
    # de empate na nota, a estabilidade preserva a ordem alfabética.
    por_nome = sorted(alunos, key=lambda a: a[0])
    por_nota_e_nome = sorted(por_nome, key=lambda a: a[1])

    return por_nota, por_nota_e_nome
