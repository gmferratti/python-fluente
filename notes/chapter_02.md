# Capítulo 02: Uma Coleção de Sequências

## 2.2 Visão Geral das Sequências Builtin

Heranças ideológicas que o Python pegou da linguagem ABC:

- Operações genéricas com diferentes tipos de sequência
- Tipos `tuple` e mapeamento builtin
- Estrutura indentada
- Tipagem forte sem declaração de variáveis

---

### Classificação por layout de memória

**Sequências de contêiner**: armazenam referências (ponteiros) para objetos de qualquer tipo,
incluindo contêineres aninhados. Exemplos: `list`, `tuple`, `collections.deque`.

**Sequências planas**: armazenam o valor do item diretamente em seu próprio bloco de memória
contíguo, sem referências. Só suportam tipos primitivos (números, caracteres, bytes).
Exemplos: `str`, `bytes`, `bytearray`, `memoryview`, `array.array`.

> Por armazenar o dado em si (e não um ponteiro), sequências planas são mais econômicas
> em memória do que sequências de contêiner equivalentes.

> **Obs.:** Uma sequência de contêiner guarda, internamente, ponteiros para objetos
> alocados no heap. Uma sequência plana elimina essa indireção e armazena os valores
> primitivos diretamente no bloco da sequência.

---

### Classificação por mutabilidade

**Sequências mutáveis**: o conteúdo pode ser modificado após a criação (`abc.MutableSequence`):
`list`, `bytearray`, `array.array`, `collections.deque`, `memoryview`.

**Sequências imutáveis**: uma vez criadas, não permitem inserção, remoção ou substituição
de itens (`abc.Sequence`): `tuple`, `str`, `bytes`.

> Em Python, o tipo mais fundamental de sequência é a `list`: um contêiner mutável.

---

## 2.3 Listcomps e Genexps

### Convenções de formatação com delimitadores

Dentro de `[]`, `()` ou `{}` pode-se quebrar a linha livremente sem usar `\`.
Um espaço acidental após `\` quebra o código silenciosamente: EVITAR.

Sempre usar vírgula de cortesia (*trailing comma*) ao final de coleções multilinhas:

o Python ignora a vírgula extra, e o próximo desenvolvedor pode adicionar ou reordenar
itens sem precisar alterar a linha anterior.

```python
cores = [
    "preto",
    "branco",
    "cinza",   # trailing comma
]
```

---

### List Comprehensions (listcomps)

Listcomps constroem novas listas de forma expressiva e são mais Pythônicas do que
combinar `map` + `filter`.

```python
symbols = "café"

# Com map/filter:
result = list(filter(lambda c: ord(c) > 127, map(str.upper, symbols)))

# Com listcomp, BEM mais legível:
result = [str.upper(c) for c in symbols if ord(c) > 127]
```

> No Python 3, variáveis declaradas dentro de uma listcomp têm escopo próprio
> e não vazam para o escopo externo.

---

### Walrus Operator (`:=`) em listcomps

O operador morsa (`:=`, pg. 47) atribui e reutiliza um valor calculado dentro da
mesma expressão, evitando cálculos duplicados:

```python
# Sem walrus: ord(c) é calculado duas vezes:
result = [ord(c) for c in symbols if ord(c) > 127]

# Com walrus: calcula uma vez e reutiliza:
result = [code for c in symbols if (code := ord(c)) > 127]
```

Obs. Debater sobre isso, pg. 47.

---

### Produto cartesiano com listcomps

Dois `for` dentro de uma listcomp geram o produto cartesiano entre duas sequências:

```python
cores = ["preto", "branco"]
tamanhos = ["S", "M", "L"]

camisetas = [(cor, tam) for cor in cores for tam in tamanhos]
# [('preto', 'S'), ('preto', 'M'), ('preto', 'L'),
#  ('branco', 'S'), ('branco', 'M'), ('branco', 'L')]
```

> O laço mais à esquerda é o mais externo. Ou seja, a ordem dos `for` define a ordem dos itens na tupla.

---

### Generator Expressions (genexps)

Genexps usam a mesma sintaxe de listcomps, mas com `()` no lugar de `[]`.
Implementam o protocolo de iterador: produzem **um item por vez** (avaliação preguiçosa ou *lazy evaulation*)
e nunca constroem uma lista completa em memória.

```python
import array

# Listcomp: constrói a lista inteira antes de passar ao construtor:
array.array("I", [ord(c) for c in symbols])

# Genexp: passa um item por vez; a lista intermediária nunca existe:
array.array("I", (ord(c) for c in symbols))
```

Produto cartesiano com genexp é o mais adequado quando o resultado será apenas iterado e você não precisa da lista final.

```python
for camiseta in (f"{cor} {tam}" for cor in cores for tam in tamanhos):
    print(camiseta)
```

> Use **genexp** quando o resultado será consumido uma única vez (argumento de função,
> loop sem reuso). Use **listcomp** quando precisar de indexação, `len()`, ou iterar
> mais de uma vez.

## 2.4 Tuplas

## 2.5 Descompactando Coleções

## 2.6 Pattern Matching com Sequências

## 2.7 Fatiamento

## 2.8 Usando "+" e "*" com sequências

## 2.9 .sort() VS sorted()

## 2.10 arrays: quando uma lista não é a resposta

## RESUMO GERAL