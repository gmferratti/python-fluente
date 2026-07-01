"""
Conjuntos (3.9).

`set`/`frozenset` guardam elementos únicos e hashable. Além de remover
duplicatas, a álgebra de conjuntos como operadores infixos evita laços
explícitos ao comparar coleções (o padrão "agulhas no palheiro").
"""


def remove_duplicatas_sem_ordem():
    """`set(l)` remove duplicatas, mas não preserva a ordem original."""
    l = ["spam", "spam", "eggs", "spam", "bacon", "eggs"]
    return set(l)


def remove_duplicatas_preservando_ordem():
    """`dict.fromkeys` remove duplicatas preservando a ordem de 1ª ocorrência."""
    l = ["spam", "spam", "eggs", "spam", "bacon", "eggs"]
    return list(dict.fromkeys(l).keys())


def agulhas_no_palheiro(needles, haystack):
    """`len(needles & haystack)` substitui um laço explícito de contagem."""
    needles, haystack = set(needles), set(haystack)

    com_set = len(needles & haystack)

    com_for = 0
    for n in needles:
        if n in haystack:
            com_for += 1

    assert com_set == com_for
    return com_set


def literais_e_comprehension_de_set():
    """`{}` é dict vazio; `set()` é o construtor para o set vazio."""
    s = {1, 2, 3}
    vazio = set()
    quadrados = {n**2 for n in range(6)}
    return s, vazio, quadrados


def operacoes_de_conjunto():
    """Interseção, união, diferença e diferença simétrica como operadores."""
    s = {1, 2, 3, 4}
    z = {3, 4, 5, 6}
    return {
        "intersecao": s & z,
        "uniao": s | z,
        "diferenca": s - z,
        "diferenca_simetrica": s ^ z,
        "subconjunto": {1, 2} <= s,
        "disjuntos": s.isdisjoint({100, 200}),
    }
