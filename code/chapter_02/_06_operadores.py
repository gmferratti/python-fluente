"""
`+`, `*`, `+=`, `*=` com sequências (2.8).

`+` e `*` sempre criam uma sequência nova. `[x] * n` com item mutável repete
a MESMA referência `n` vezes; `[x for _ in range(n)]` cria `n` objetos
distintos. `+=` modifica no lugar quando o objeto implementa `__iadd__`
(list); senão cai em `__add__` e cria um objeto novo (tuple).
"""


def board_bug_referencia_compartilhada():
    """`[x] * n` com item mutável compartilha a MESMA referência."""
    board = [["_"] * 3] * 3
    board[1][2] = "X"
    return board  # as três linhas mudam: bug


def board_correto_com_listcomp():
    """`for` cria um objeto novo a cada iteração, sem compartilhar referência."""
    board = [["_"] * 3 for _ in range(3)]
    board[1][2] = "X"
    return board  # só a linha 1 muda: correto


def iadd_lista_vs_tupla():
    """`+=` numa lista modifica no lugar; numa tupla, cria objeto novo."""
    l = [1, 2, 3]
    id_antes_lista = id(l)
    l += [4, 5]
    lista_mesmo_id = id(l) == id_antes_lista

    t = (1, 2, 3)
    id_antes_tupla = id(t)
    t += (4, 5)
    tupla_mesmo_id = id(t) == id_antes_tupla

    return lista_mesmo_id, tupla_mesmo_id


def iadd_em_item_mutavel_dentro_de_tupla():
    """`t[i] += ...` pode alterar o conteúdo e ainda lançar TypeError."""
    t = (1, 2, [30, 40])
    try:
        t[2] += [50, 60]
    except TypeError as exc:
        return t, repr(exc)  # a lista interna já foi alterada apesar do erro
    raise AssertionError("esperava TypeError")
