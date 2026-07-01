"""
Demonstrações executáveis do capítulo 03.

Execute diretamente:
    python -m chapter_03.demo
"""

from . import _01_dict_comprehensions as dict_comprehensions
from . import _02_pattern_matching as pattern_matching
from . import _03_setdefault as setdefault
from . import _04_missing_and_defaultdict as missing_and_defaultdict
from . import _05_dict_variants as dict_variants
from . import _06_immutable_mappings as immutable_mappings
from . import _07_dict_views as dict_views
from . import _08_sets as sets
from . import _09_dict_views_as_sets as dict_views_as_sets


def demo_dict_comprehensions():
    print("=== dictcomp: país -> código ===")
    print(dict_comprehensions.dictcomp_pais_para_codigo())

    print("\n=== dictcomp com filtro ===")
    print(dict_comprehensions.dictcomp_com_filtro())

    print("\n=== ** em chamada de função ===")
    print(dict_comprehensions.star_star_em_chamada_de_funcao())

    print("\n=== ** em literal dict (última chave vence) ===")
    print(dict_comprehensions.star_star_em_literal_dict())

    print("\n=== | cria novo dict; |= modifica no lugar ===")
    print(dict_comprehensions.merge_com_pipe())


def demo_pattern_matching():
    print("\n=== match/case sobre mapeamentos ===")
    print(pattern_matching.get_creators({"type": "book", "api": 2, "authors": ["Martelli"]}))
    print(pattern_matching.get_creators({"type": "movie", "director": "Greta Gerwig"}))

    print("\n=== chave extra não mencionada ainda casa ===")
    print(pattern_matching.registro_com_chave_extra_ainda_casa())

    print("\n=== **details captura o resto do padrão ===")
    print(pattern_matching.capturar_chaves_extras({"category": "ice cream", "flavor": "vanilla"}))


def demo_setdefault():
    print("\n=== hashabilidade ===")
    print(setdefault.exemplos_de_hashabilidade())

    pares = [("python", 1), ("java", 2), ("python", 3)]
    print("\n=== índice com get()+set() vs setdefault() ===")
    print(setdefault.indice_com_get_e_atualizacao(pares))
    print(setdefault.indice_com_setdefault(pares))


def demo_missing_and_defaultdict():
    pares = [("python", 1), ("java", 2), ("python", 3)]
    print("\n=== defaultdict(list) ===")
    print(dict(missing_and_defaultdict.indice_com_defaultdict(pares)))

    print("\n=== StrKeyDict0: chave numérica e string equivalentes ===")
    print(missing_and_defaultdict.str_key_dict0_aceita_chave_numerica_ou_string())


def demo_dict_variants():
    print("\n=== ChainMap: busca em cascata, escreve só no primeiro ===")
    print(dict_variants.chainmap_busca_em_cascata())

    print("\n=== Counter: most_common ===")
    print(dict_variants.counter_contagem_e_most_common())

    print("\n=== StrKeyDict (UserDict): update() também converte chaves ===")
    print(dict_variants.str_key_dict_converte_chaves_no_update())


def demo_immutable_mappings():
    print("\n=== MappingProxyType: somente leitura, mas dinâmico ===")
    print(immutable_mappings.mappingproxy_e_somente_leitura_mas_dinamico())


def demo_dict_views():
    print("\n=== view reflete mudança no dict original ===")
    print(dict_views.view_reflete_mudanca_no_dict_original())

    print("\n=== view não é indexável ===")
    print(dict_views.view_nao_e_indexavel())


def demo_sets():
    print("\n=== remover duplicatas (com e sem ordem) ===")
    print(sets.remove_duplicatas_sem_ordem())
    print(sets.remove_duplicatas_preservando_ordem())

    print("\n=== agulhas no palheiro ===")
    print(sets.agulhas_no_palheiro([1, 2, 3], [2, 3, 4, 5]))

    print("\n=== literais e comprehension de set ===")
    print(sets.literais_e_comprehension_de_set())

    print("\n=== operações de conjunto ===")
    print(sets.operacoes_de_conjunto())


def demo_dict_views_as_sets():
    print("\n=== chaves em comum entre dois dicts ===")
    print(dict_views_as_sets.chaves_em_comum_entre_dois_dicts())

    print("\n=== chaves em comum com um set comum ===")
    print(dict_views_as_sets.chaves_em_comum_com_set_comum())


if __name__ == "__main__":
    demo_dict_comprehensions()
    demo_pattern_matching()
    demo_setdefault()
    demo_missing_and_defaultdict()
    demo_dict_variants()
    demo_immutable_mappings()
    demo_dict_views()
    demo_sets()
    demo_dict_views_as_sets()
