"""
Pattern matching com sequências (2.6).

`match/case` descreve a forma esperada dos dados (tamanho, tipos, valores) de
uma vez, no lugar de encadear isinstance()/len()/índices manualmente.
"""

from ._03_desempacotamento import METRO_AREAS


def pattern_matching_metro_areas():
    """Exemplo do livro: match/case + guard clause sobre METRO_AREAS."""
    linhas = []
    for record in METRO_AREAS:
        match record:
            case [name, _, _, (lat, lon)] if lon <= 0:
                linhas.append(f"{name:15} | {lat:9.4f} | {lon:9.4f}")
    return linhas
