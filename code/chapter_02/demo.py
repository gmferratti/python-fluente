"""
Demonstrações executáveis do capítulo 02.

Execute diretamente:
    python -m chapter_02.demo
"""

from . import _01_comprehensions as comprehensions
from . import _02_tuplas as tuplas
from . import _03_desempacotamento as desempacotamento
from . import _04_pattern_matching as pattern_matching
from . import _05_fatiamento as fatiamento
from . import _06_operadores as operadores
from . import _07_ordenacao as ordenacao
from . import _08_estruturas_especializadas as estruturas_especializadas


def demo_comprehensions():
    print("=== listcomp vs map/filter ===")
    print(comprehensions.listcomp_vs_map_filter())

    print("\n=== walrus operator em listcomp ===")
    print(comprehensions.walrus_em_listcomp())

    print("\n=== produto cartesiano (listcomp) ===")
    print(comprehensions.produto_cartesiano_listcomp())

    print("\n=== genexp: array sem lista intermediária ===")
    print(comprehensions.genexp_construcao_array())

    print("\n=== produto cartesiano (genexp) ===")
    for camiseta in comprehensions.produto_cartesiano_genexp():
        print(camiseta)


def demo_tuplas():
    print("\n=== tuplas como registros ===")
    print(tuplas.tuplas_como_registros())

    print("\n=== desempacotamento posicional ===")
    print(tuplas.desempacotamento_posicional())

    print("\n=== memória: tupla vs lista ===")
    print(tuplas.memoria_tupla_vs_lista())

    print("\n=== tuplas com itens mutáveis ===")
    print(tuplas.tuplas_com_itens_mutaveis())

    print("\n=== tupla com mutável não é hashable ===")
    print(tuplas.tupla_com_mutavel_nao_e_hashable())


def demo_desempacotamento():
    print("\n=== path split ===")
    print(desempacotamento.unpacking_path_split())

    print("\n=== * recolhe o excesso ===")
    print(desempacotamento.star_recolhe_excesso())

    print("\n=== * em chamadas e literais (PEP 448) ===")
    print(desempacotamento.star_em_chamadas_e_literais())

    print("\n=== desempacotamento aninhado ===")
    print(desempacotamento.desempacotamento_aninhado())


def demo_pattern_matching():
    print("\n=== match/case sobre METRO_AREAS ===")
    for linha in pattern_matching.pattern_matching_metro_areas():
        print(linha)


def demo_fatiamento():
    print("\n=== fatias nomeadas (invoice) ===")
    for descricao, preco in fatiamento.fatias_nomeadas_invoice():
        print(preco, descricao)

    print("\n=== atribuindo a uma fatia ===")
    print(fatiamento.atribuindo_a_uma_fatia())


def demo_operadores():
    print("\n=== bug: [x] * n com item mutável ===")
    print(operadores.board_bug_referencia_compartilhada())

    print("\n=== correto: listcomp cria objetos distintos ===")
    print(operadores.board_correto_com_listcomp())

    print("\n=== += lista (no lugar) vs tupla (objeto novo) ===")
    print(operadores.iadd_lista_vs_tupla())

    print("\n=== += num item mutável dentro de uma tupla ===")
    print(operadores.iadd_em_item_mutavel_dentro_de_tupla())


def demo_ordenacao():
    print("\n=== sort() devolve None ===")
    print(ordenacao.sort_devolve_none())

    print("\n=== reverse e key ===")
    print(ordenacao.sorted_com_reverse_e_key())

    print("\n=== estabilidade do Timsort ===")
    print(ordenacao.sorted_e_estavel())


def demo_estruturas_especializadas():
    print("\n=== array: valores crus, sem indireção ===")
    print(estruturas_especializadas.array_de_floats(5))

    print("\n=== memoryview: mesma memória, outro formato ===")
    print(estruturas_especializadas.memoryview_sobre_array())

    print("\n=== deque: rotate ===")
    print(estruturas_especializadas.deque_rotate())

    print("\n=== deque: buffer circular (maxlen) ===")
    print(estruturas_especializadas.deque_buffer_circular())

    try:
        print("\n=== numpy: distância euclidiana vetorizada ===")
        print(estruturas_especializadas.numpy_distancia_euclidiana())
    except ModuleNotFoundError:
        print("\n=== numpy não instalado: pulando exemplos vetorizados ===")


if __name__ == "__main__":
    demo_comprehensions()
    demo_tuplas()
    demo_desempacotamento()
    demo_pattern_matching()
    demo_fatiamento()
    demo_operadores()
    demo_ordenacao()
    demo_estruturas_especializadas()
