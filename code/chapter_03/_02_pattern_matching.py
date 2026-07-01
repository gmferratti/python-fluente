"""
Pattern matching com mapeamentos (3.2).

`match/case` sobre um dict casa por chave de forma parcial: chaves do sujeito
que não aparecem no padrão não impedem o match. `**resto` captura as chaves
não mencionadas explicitamente e deve ser o último item do padrão.
"""


def get_creators(record: dict) -> list:
    """Extrai autores/diretor de um registro de livro ou filme.

    A ordem dos `case` importa: primeiro a API nova de livros, depois a
    antiga, depois qualquer outro registro de livro (formato inválido),
    e por fim filmes.
    """
    match record:
        case {"type": "book", "api": 2, "authors": [*names]}:
            return names
        case {"type": "book", "api": 1, "author": name}:
            return [name]
        case {"type": "book"}:
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {"type": "movie", "director": name}:
            return [name]
        case _:
            raise ValueError(f"Invalid record: {record!r}")


def capturar_chaves_extras(food: dict):
    """`**details` recolhe as chaves não mencionadas no padrão."""
    match food:
        case {"category": "ice cream", **details}:
            return details
    return None


def registro_com_chave_extra_ainda_casa():
    """Uma chave extra ('title') não mencionada no padrão não impede o match."""
    record = {
        "type": "book", "api": 2, "authors": ["Martelli", "Ravenscroft"],
        "title": "Python in a Nutshell",
    }
    return get_creators(record)
