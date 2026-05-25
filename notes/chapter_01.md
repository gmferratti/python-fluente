# Capítulo 01: O Modelo de Dados do Python

## A ideia que estrutura o livro

Python tem um conjunto de protocolos: se um objeto implementa `__len__`, `len()` funciona. Se implementa `__getitem__`, indexação e iteração funcionam. O interpretador não verifica tipo — ele tenta chamar o método. Se existir, a operação funciona. Se não existir, levanta `TypeError`.

Esses métodos se chamam **métodos especiais** (ou *dunder methods*, de *double underscore*). O nome informal "métodos mágicos" é evitado pelo Ramalho — não há magia, é um protocolo deliberado e documentado.

Uma regra importante: você implementa, o interpretador invoca. Em geral, você nunca chama `x.__len__()` diretamente — chama `len(x)`, que além de invocar `__len__` pode aplicar otimizações extras. A única exceção comum é `__init__`, chamado via `super().__init__()` em herança.

---

## FrenchDeck: o exemplo principal

O baralho é construído com apenas dois dunders:

```python
def __len__(self):
    return len(self._cards)

def __getitem__(self, position):
    return self._cards[position]
```

Com isso, a classe ganha de graça:

| Operação | Por que funciona |
|---|---|
| `len(deck)` | chama `__len__` |
| `deck[0]`, `deck[-1]`, `deck[1:3]` | chama `__getitem__` |
| `for card in deck` | chama `__getitem__` a partir do índice 0 |
| `reversed(deck)` | idem, de trás para frente |
| `card in deck` | percorre via `__getitem__` até encontrar |
| `random.choice(deck)` | usa `__len__` + `__getitem__` |
| `sorted(deck, key=fn)` | itera via `__getitem__` |

`FrenchDeck` não herda de `list`, não herda de `Sequence` — mas se comporta como sequência em todos esses contextos. Isso é duck typing.

---

## Duck typing e protocolos

> "If it walks like a duck and quacks like a duck, then it's a duck."

O interpretador não pergunta "esse objeto é uma sequência?" antes de iterar. Ele tenta chamar `__getitem__`. Se funcionar, é uma sequência para fins práticos.

Em linguagens de tipagem estática você precisaria declarar `implements Sequence`. Em Python, você só precisa *ter o método*. Você não herda comportamento — você o *anuncia* implementando os métodos que o protocolo espera.

**Protocolo informal** é o nome para esse acordo implícito. O protocolo de sequência, por exemplo, exige `__len__` e `__getitem__`. Não há interface para declarar — mas o acordo é totalmente previsível e documentado.

Para casos onde você precisa de garantias mais formais, existem as ABCs (`collections.abc`):

| | Protocolo informal (duck typing) | ABC (goose typing) |
|---|---|---|
| Como funciona | implementa os métodos; o interpretador usa | herda de `collections.abc.Sequence` ou registra |
| Verificação | em tempo de execução, na chamada | `isinstance()` retorna `True` mesmo sem herança direta |
| Quando usar | maioria dos casos | quando quer garantias formais ou documentação explícita do contrato |

ABCs são explorados nos capítulos de coleções. Por enquanto, o que importa é entender que elas existem para formalizar o que os protocolos informais já fazem na prática.

---

## namedtuple

```python
Card = collections.namedtuple("Card", ['rank', 'suit'])
```

Cria uma subclasse imutável de `tuple` com campos nomeados. A escolha aqui é intencional: `Card` é um objeto de valor puro — só agrupa `rank` e `suit`, sem comportamento próprio. Instâncias são acessadas por nome (`card.rank`) ou índice (`card[0]`), e desempacotáveis como tuplas normais.

| Tipo | Mutável | Métodos | Defaults complexos | Uso típico |
|---|---|---|---|---|
| `namedtuple` | não | limitado | não | objetos de valor simples, imutáveis |
| `dataclass` | sim (padrão) | sim | sim | entidades com comportamento |
| `TypedDict` | sim | não | não | dicionários tipados |

---

## __setitem__ e random.shuffle

`random.shuffle()` troca elementos por posição: internamente faz `deck[i] = deck[j]`. Sem `__setitem__`, isso lança `TypeError`. Com uma linha, o problema some:

```python
def __setitem__(self, position, value):
    self._cards[position] = value
```

Esse é o padrão do modelo de dados: você entrega um método, o Python entrega um comportamento. Não precisa saber como `shuffle` funciona internamente — só precisa entender o que o protocolo exige.

---

## Por que len() não é um método?

Praticidade vence a pureza. Para tipos built-in como `list` e `str`, `len()` lê diretamente um campo da struct C subjacente — O(1) sem overhead de chamada de método. Se fosse um método comum, esse atalho não seria possível.

Implementar `__len__` na sua classe garante que `len()` funcione da mesma forma consistente. A regra geral vale para todos os dunders: prefira a função built-in ao método direto. `len(x)` em vez de `x.__len__()`.

---

## Vector: métodos aritméticos e de representação

O segundo exemplo do capítulo mostra os dunders de aritmética:

```python
v1 = Vector(2, 4)
repr(v1)   # chama __repr__
abs(v1)    # chama __abs__
bool(v1)   # chama __bool__
v1 + v2    # chama __add__
v1 * 3     # chama __mul__
```

O Python não cria operadores novos — você sobrescreve o comportamento dos existentes para seus tipos. `v1 + v2` chama `v1.__add__(v2)`. Operadores como `@` (produto matricial, PEP 465) funcionam da mesma forma via `__matmul__`.

**`__repr__` vs `__str__`:** prefira implementar `__repr__`. Ele aparece no console interativo, dentro de coleções e em mensagens de erro — contextos que importam para quem está debugando. `__str__` é chamado por `print()`, mas quando não está definido o Python usa `__repr__` como fallback. O inverso não acontece.

O `!r` em f-strings aplica `repr()` ao valor — importante para que strings apareçam com aspas e tipos especiais sejam identificáveis:

```python
def __repr__(self):
    return f"Vector({self.x!r}, {self.y!r})"
```

---

## O princípio maior

Ruby e Python expõem um **protocolo de metaobjetos** rico: qualquer desenvolvedor pode emular o que os mantenedores do interpretador fazem. Tipos definidos pelo usuário têm acesso aos mesmos ganchos que os tipos built-in.

É por isso que `FrenchDeck` funciona com `random.choice()` sem herdar de `list`, e `Vector` pode usar `+` sem herdar de nenhum tipo numérico. Não é privilégio dos tipos nativos — é um protocolo aberto.

O capítulo 1 introduz esse princípio cedo porque é a base de tudo que vem depois no livro.

---

## Resumo

```python
# __len__ + __getitem__  →  len(), índice, slicing, iteração, reversed(), in, choice(), sorted()
# + __setitem__          →  shuffle() e atribuição por índice
# + __contains__         →  sobrescreve a busca linear do "in" com lógica própria
# + __iter__             →  sobrescreve a iteração via __getitem__
# + __reversed__         →  sobrescreve o reversed() via __getitem__
```

---

## Referência: mapa dos métodos especiais

```
REPRESENTAÇÃO E CICLO DE VIDA
  __init__          construção da instância
  __new__           criação do objeto (antes do __init__)
  __del__           destruição (garbage collection)
  __repr__          repr() — representação para desenvolvedor
  __str__           str() — representação legível para usuário
  __format__        format() e f-strings
  __bytes__         bytes()
  __bool__          bool() — verdadeiro/falso do objeto

COMPARAÇÃO
  __eq__   ==       __ne__   !=
  __lt__   <        __le__   <=
  __gt__   >        __ge__   >=
  __hash__          hash() — necessário quando __eq__ é definido

OPERADORES ARITMÉTICOS (infixos)
  __add__    +      __radd__     +  (lado direito)
  __sub__    -      __mul__      *
  __truediv__ /     __floordiv__ //
  __mod__    %      __pow__      **
  __matmul__ @      (produto matricial, PEP 465)

OPERADORES UNÁRIOS
  __neg__    -x     __pos__  +x     __abs__  abs(x)     __invert__  ~x

COLEÇÕES E SEQUÊNCIAS
  __len__           len()
  __getitem__       obj[key], slicing
  __setitem__       obj[key] = value
  __delitem__       del obj[key]
  __contains__      in (busca otimizada; fallback é __getitem__)
  __iter__          for item in obj
  __reversed__      reversed()
  __next__          próximo item de um iterator
  __missing__       dict subclass: chave ausente

CONTEXTO (with)
  __enter__         entrada do bloco with
  __exit__          saída do bloco with (inclusive por exceção)

CHAMADA
  __call__          obj() — torna a instância chamável como função

ATRIBUTOS
  __getattr__       acesso a atributo não encontrado normalmente
  __setattr__       qualquer atribuição de atributo
  __delattr__       del obj.attr
  __getattribute__  todo acesso a atributo (cuidado: fácil loop infinito)
  __dir__           dir()
```
