# Capítulo 01: O Modelo de Dados do Python

## Conceito central

O **modelo de dados** é a API que o Python expõe para que objetos criados pelo usuário se integrem à linguagem como cidadãos de primeira classe. Isso é feito via **métodos especiais** (dunder methods), que o interpretador chama automaticamente em resposta a operações da linguagem (`len(x)`, `x[0]`, `for item in x`, etc.).

---

## Métodos especiais (dunder methods)

- São identificados por duplo underline no início e no fim: `__len__`, `__getitem__`, `__repr__`, etc. O nome informal "métodos mágicos" é evitado pelo autor — não há magia, é um protocolo deliberado.
- **Não são chamados diretamente pelo seu código.** Você implementa; o interpretador invoca. A exceção mais comum é `__init__`, que você chama via `super().__init__()` em herança.
- Quando precisar invocar o comportamento, use a função embutida correspondente: `len(x)` em vez de `x.__len__()`. As funções embutidas geralmente aplicam otimizações extras.
- A lista completa está documentada no Python Data Model (capítulo da documentação oficial).

### Mapa dos métodos especiais por categoria

```
REPRESENTACAO E CICLO DE VIDA
  __init__        construcao da instancia
  __new__         criacao do objeto (antes do __init__)
  __del__         destruicao (garbage collection)
  __repr__        repr() — representacao para desenvolvedor
  __str__         str() — representacao legivel para usuario
  __format__      format() e f-strings
  __bytes__       bytes()
  __bool__        bool() — verdadeiro/falso do objeto

COMPARACAO
  __eq__   ==     __ne__  !=
  __lt__   <      __le__  <=
  __gt__   >      __ge__  >=
  __hash__        hash() — necessario quando __eq__ e definido

OPERADORES ARITMETICOS (infixos)
  __add__    +    __radd__   +  (lado direito)
  __sub__    -    __mul__    *
  __truediv__ /   __floordiv__ //
  __mod__    %    __pow__    **
  __matmul__ @    (produto matricial, PEP 465)

OPERADORES UNARIOS
  __neg__    -x   __pos__  +x   __abs__  abs(x)   __invert__  ~x

COLECOES E SEQUENCIAS
  __len__         len()
  __getitem__     obj[key], slicing
  __setitem__     obj[key] = value
  __delitem__     del obj[key]
  __contains__    in (busca otimizada; fallback e __getitem__)
  __iter__        for item in obj
  __reversed__    reversed()
  __next__        proximo item de um iterator
  __missing__     dict subclass: chave ausente

CONTEXTO (with)
  __enter__       entrada do bloco with
  __exit__        saida do bloco with (inclusive por excecao)

CHAMADA
  __call__        obj()  — torna a instancia chamavel como funcao

ATRIBUTOS
  __getattr__     acesso a atributo nao encontrado normalmente
  __setattr__     qualquer atribuicao de atributo
  __delattr__     del obj.attr
  __getattribute__ todo acesso a atributo (cuidado: facil loop infinito)
  __dir__         dir()
```

### Por que `len()` não é um método?

Praticidade vence a pureza. Para tipos embutidos como `list` e `str`, `len()` lê diretamente um campo da struct C subjacente — é O(1) sem overhead de chamada de método. Implementar `__len__` na sua classe garante que `len()` funcione do mesmo jeito, mantendo a consistência da linguagem.

---

## namedtuple

```python
Card = collections.namedtuple("Card", ['rank', 'suit'])
```

- Cria uma **subclasse imutável de tuple** cujos campos têm nomes. Ideal para agrupamento de atributos sem comportamento próprio (objetos de valor puros).
- Não confundir com `dataclass` (mutável por padrão, suporta métodos e defaults complexos) nem com `TypedDict` (para dicionários tipados).
- Instâncias são acessadas por nome (`card.rank`) ou por índice (`card[0]`), e são desempacotáveis como tuplas normais.

---

## Protocolos e duck typing

### O que é duck typing

> "If it walks like a duck and quacks like a duck, then it's a duck."

Duck typing é a prática de determinar se um objeto é adequado para um uso **pelo que ele faz**, não **pelo que ele é**. Em Python, o interpretador não verifica o tipo de `x` antes de chamar `len(x)` — ele simplesmente tenta chamar `x.__len__()`. Se existir, funciona. Se não existir, levanta `TypeError`.

Isso contrasta com linguagens de tipagem estática (Java, C#), onde você precisaria declarar que sua classe implementa uma interface (`implements Sequence`) para que o compilador aceitasse o objeto em determinados contextos.

**Consequência prática:** você não herda comportamento em Python — você *anuncia* comportamento implementando os métodos que o protocolo espera. Qualquer código que dependa de `len()` vai funcionar com sua classe, desde que ela tenha `__len__`.

### Protocolos informais vs. ABCs

| | Protocolo informal (duck typing) | ABC (goose typing) |
|---|---|---|
| Como funciona | implementa os métodos; o interpretador usa | herda de `collections.abc.Sequence` ou registra |
| Verificação | em tempo de execução, na chamada | `isinstance()` retorna `True` mesmo sem herança direta |
| Quando usar | maioria dos casos | quando você quer garantias formais ou documentação explícita do contrato |

### FrenchDeck como exemplo

Ao implementar `__len__` e `__getitem__`, a classe `FrenchDeck` ganhou automaticamente:

| Operação | Como funciona |
|---|---|
| `len(deck)` | chama `__len__` |
| `deck[0]`, `deck[-1]`, `deck[1:3]` | chama `__getitem__` |
| `for card in deck` | chama `__getitem__` a partir do índice 0 |
| `reversed(deck)` | idem, de trás para frente |
| `card in deck` | percorre via `__getitem__` até encontrar ou esgotar |
| `random.choice(deck)` | usa `__len__` + `__getitem__` |
| `sorted(deck, key=fn)` | itera via `__getitem__` |

`FrenchDeck` não herda de `list`, não herda de `Sequence` — mas se comporta como uma sequência em todos esses contextos. Isso é duck typing em ação.

---

## __setitem__ e mutabilidade

Sem `__setitem__`, `random.shuffle(deck)` lança `TypeError` porque o shuffle precisa trocar elementos por posição. Basta uma linha:

```python
def __setitem__(self, position, value):
    self._cards[position] = value
```

---

## ABCs ou Classes Base Abstratas

- Definidas em `collections.abc` (e `numbers`). Documentam formalmente os protocolos do Python: `Sequence`, `Mapping`, `Iterable`, `MutableSequence`, etc.
- Permitem verificar conformidade com `isinstance(obj, Sequence)` sem herança direta, desde que os métodos necessários estejam implementados (registro virtual).
- O capítulo os menciona como antecipação; são explorados em profundidade nos capítulos de coleções e classes abstratas.

---

## Operadores infixos e unários

- **Unários**: operam sobre um único operando. `abs(v)` chama `v.__abs__()`. `len(x)` se comporta de forma análoga para sequências.
- **Infixos**: operam entre dois operandos. `v1 + v2` chama `v1.__add__(v2)`. Graças à sobrecarga, tipos como vetores e matrizes podem usar `+`, `*`, `@` (produto matricial, PEP 465) de forma natural.
- O Python não cria operadores novos — sobrescreve o comportamento dos existentes para tipos definidos pelo usuário.

---

## Metaobjetos e a filosofia do Python

Ruby e Python expõem um **protocolo de metaobjetos** (MOP) rico: qualquer pessoa pode emular o que os mantenedores do interpretador fazem. Não é mágica — é design deliberado para que a linguagem seja extensível de forma coerente. Isso contrasta com linguagens onde os tipos primitivos têm privilégios que classes de usuário não têm.

O capítulo 1 já introduz esse princípio porque é o fundamento de tudo que vem depois no livro.


# Adicionar __contains__ sobrescreve a busca linear do "in" com logica propria.
# Adicionar __iter__ sobrescreve a iteracao via __getitem__.
# Adicionar __reversed__ sobrescreve o reversed() via __getitem__.
```
