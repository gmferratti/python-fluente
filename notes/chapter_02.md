# Capítulo 02: Uma Coleção de Sequências

## Resumo Geral

O capítulo percorre as sequências builtin do Python sob quatro eixos: como são organizadas na memória (contêiner vs. plana), como se comportam quanto à mutabilidade, quais atalhos sintáticos existem para criá-las e desempacotá-las, e quando vale a pena trocar `list` por uma estrutura mais especializada.

- **2.2** classifica as sequências por layout de memória e por mutabilidade.
- **2.3** cobre listcomps e genexps como formas mais expressivas de construir sequências.
- **2.4** trata tuplas em seus dois papéis: lista imutável e registro com campos posicionais.
- **2.5** expande o desempacotamento (`*`, `**`, aninhado) além da atribuição simples.
- **2.6** introduz `match/case` como uma forma declarativa de checar a forma dos dados.
- **2.7** detalha o fatiamento: a convenção meio-aberta, índices negativos, passo e o objeto `slice`.
- **2.8** examina pegadinhas de `+`, `*`, `+=` e `*=`, sobretudo com itens mutáveis.
- **2.9** compara `list.sort()` (no lugar) com `sorted()` (cópia nova).
- **2.10** apresenta alternativas à `list` para casos especializados: `array`, `memoryview`, NumPy e `deque`.

Os exemplos de código mais extensos ou executáveis estão em [`code/chapter_02/`](../code/chapter_02/); aqui ficam apenas os trechos curtos que ilustram um ponto específico do texto.

---

## 2.2 Visão Geral das Sequências Builtin

Heranças ideológicas que o Python pegou da linguagem ABC:

- Operações genéricas com diferentes tipos de sequência
- Tipos `tuple` e mapeamento builtin
- Estrutura indentada
- Tipagem forte sem declaração de variáveis

### 2.2.1 Classificação por layout de memória

**Sequências de contêiner**: armazenam referências (ponteiros) para objetos de qualquer tipo, incluindo contêineres aninhados. Exemplos: `list`, `tuple`, `collections.deque`.

**Sequências planas**: armazenam o valor do item diretamente em seu próprio bloco de memória contíguo, sem referências. Só suportam tipos primitivos (números, caracteres, bytes). Exemplos: `str`, `bytes`, `bytearray`, `memoryview`, `array.array`.

> Por armazenar o dado em si, e não um ponteiro, sequências planas são mais econômicas em memória do que sequências de contêiner equivalentes. Uma sequência de contêiner guarda, internamente, ponteiros para objetos alocados no heap; uma sequência plana elimina essa indireção e armazena os valores primitivos diretamente no bloco da sequência.

### 2.2.2 Classificação por mutabilidade

**Sequências mutáveis**: o conteúdo pode ser modificado após a criação (`abc.MutableSequence`): `list`, `bytearray`, `array.array`, `collections.deque`, `memoryview`.

**Sequências imutáveis**: uma vez criadas, não permitem inserção, remoção ou substituição de itens (`abc.Sequence`): `tuple`, `str`, `bytes`.

> Em Python, o tipo mais fundamental de sequência é a `list`: um contêiner mutável.

---

## 2.3 Listcomps e Genexps

### 2.3.1 Convenções de formatação com delimitadores

Dentro de `[]`, `()` ou `{}` pode-se quebrar a linha livremente sem usar `\`. Um espaço acidental após `\` quebra o código silenciosamente: evitar.

Sempre usar vírgula de cortesia (*trailing comma*) ao final de coleções multilinhas. O Python ignora a vírgula extra, e o próximo desenvolvedor pode adicionar ou reordenar itens sem precisar alterar a linha anterior:

```python
cores = [
    "preto",
    "branco",
    "cinza",   # trailing comma
]
```

### 2.3.2 List Comprehensions (listcomps)

Listcomps constroem novas listas de forma expressiva e são mais Pythônicas do que combinar `map` + `filter` (comparação completa em [`_01_comprehensions.py: listcomp_vs_map_filter`](../code/chapter_02/_01_comprehensions.py)):

```python
symbols = "café"
resultado = [str.upper(c) for c in symbols if ord(c) > 127]
```

> No Python 3, variáveis declaradas dentro de uma listcomp têm escopo próprio e não vazam para o escopo externo.

### 2.3.3 Walrus Operator (`:=`) em listcomps

O operador morsa (`:=`, pg. 47) atribui e reutiliza um valor calculado dentro da mesma expressão, evitando cálculos duplicados:

```python
# Sem walrus: ord(c) é calculado duas vezes
resultado = [ord(c) for c in symbols if ord(c) > 127]

# Com walrus: calcula uma vez e reutiliza
resultado = [code for c in symbols if (code := ord(c)) > 127]
```

Obs.: debater sobre isso, pg. 47.

### 2.3.4 Produto cartesiano com listcomps

Dois `for` dentro de uma listcomp geram o produto cartesiano entre duas sequências:

```python
cores = ["preto", "branco"]
tamanhos = ["S", "M", "L"]
camisetas = [(cor, tam) for cor in cores for tam in tamanhos]
# [('preto', 'S'), ('preto', 'M'), ('preto', 'L'),
#  ('branco', 'S'), ('branco', 'M'), ('branco', 'L')]
```

> O laço mais à esquerda é o mais externo: a ordem dos `for` define a ordem dos itens na tupla.

### 2.3.5 Generator Expressions (genexps)

Genexps usam a mesma sintaxe de listcomps, com `()` no lugar de `[]`. Implementam o protocolo de iterador: produzem **um item por vez** (avaliação preguiçosa, ou *lazy evaluation*) e nunca constroem uma lista completa em memória.

```python
import array

array.array("I", (ord(c) for c in symbols))  # não cria lista intermediária
```

Produto cartesiano com genexp é o mais adequado quando o resultado será apenas iterado, sem necessidade da lista final.

> Use **genexp** quando o resultado será consumido uma única vez (argumento de função, loop sem reuso). Use **listcomp** quando precisar de indexação, `len()`, ou iterar mais de uma vez.

---

## 2.4 Tuplas

Tuplas possuem dupla função em Python: **listas imutáveis** ou **registros com campos sem nome**. A posição de cada item carrega significado quando a tupla é usada como registro.

### 2.4.1 Tuplas como registros

```python
brasilia = (-15.7797, -47.9297)     # (latitude, longitude)
lat, lon = brasilia

registro = ("São Paulo", 2024, 11_451_245)   # (cidade, ano, população)
cidade, ano, pop = registro
```

### 2.4.2 Desempacotamento posicional

```python
# Swap sem variável temporária
a, b = 10, 20
a, b = b, a  # a=20, b=10

# Ignorar campos com _ (convenção para variável descartável)
_, ano, _ = registro

# Capturar o restante com * (retorna lista, mesmo vindo de tupla)
primeiro, *meio, ultimo = (1, 2, 3, 4, 5)
# primeiro=1, meio=[2, 3, 4], ultimo=5
```

> O desempacotamento com `*` é expandido na seção 2.5.

### 2.4.3 Memória: tupla vs lista

Tupla usa menos memória do que lista. Instâncias de `list` reservam espaço extra (*overallocation*) para amortizar o custo de acréscimos futuros; `tuple` não precisa disso.

```python
sys.getsizeof((1, 2, 3, 4, 5))   # 80 bytes
sys.getsizeof([1, 2, 3, 4, 5])   # 104 bytes
```

> Use `tuple` quando a sequência não vai mudar: além de mais leve, sinaliza intenção ao leitor.

### 2.4.4 Tuplas com itens mutáveis

A imutabilidade da tupla se aplica às **referências** que ela armazena, não ao conteúdo dos objetos referenciados:

```python
t = ([1, 2], [3, 4])
t[0].append(99)  # OK: mutamos a lista interna, não a tupla
t[0] = [9, 9]     # TypeError: não podemos trocar a referência
```

> Tuplas com itens mutáveis combinam o pior dos dois mundos: não são `hashable` (logo, não servem como chave de dicionário) e ainda carregam risco de mutação acidental.

### 2.4.5 Métodos: tupla vs lista

Tupla expõe apenas `count` e `index`: sem mutabilidade, operações de modificação não fazem sentido.

| Operação              | `tuple` | `list` |
|-----------------------|:-------:|:------:|
| `count(x)`            | ✓       | ✓      |
| `index(x)`            | ✓       | ✓      |
| `len()`, `in`, `[i]`  | ✓       | ✓      |
| Fatiamento `[a:b]`    | ✓       | ✓      |
| Concatenação `+`, `*` | ✓       | ✓      |
| `append(x)`           | ✗       | ✓      |
| `insert(i, x)`        | ✗       | ✓      |
| `remove(x)`, `pop()`  | ✗       | ✓      |
| `sort()`, `reverse()` | ✗       | ✓      |
| `extend(it)`          | ✗       | ✓      |
| `clear()`, `copy()`   | ✗       | ✓      |

---

## 2.5 Descompactando Coleções

O desempacotamento (*unpacking*) extrai itens de qualquer iterável sem precisar de índices explícitos. Funciona com tuplas, listas, geradores e qualquer objeto iterável.

### 2.5.1 Desempacotamento básico e path split

```python
import os

_, filename = os.path.split("/home/user/docs/report.pdf")   # filename = "report.pdf"
*_, last = "/usr/local/bin/python".split("/")                # last = "python"
```

### 2.5.2 `*` para recolher itens em excesso

O operador `*` absorve o que sobrar e sempre retorna uma **lista**, mesmo que a sequência original seja uma tupla ou outro iterável:

```python
primeiro, *resto = range(5)             # primeiro=0, resto=[1, 2, 3, 4]
*inicio, ultimo = range(5)              # inicio=[0, 1, 2, 3], ultimo=4
primeiro, *meio, ultimo = range(6)      # primeiro=0, meio=[1, 2, 3, 4], ultimo=5
a, b, *_ = (10, 20, 30, 40, 50)         # descarta o restante explicitamente
```

### 2.5.3 `*` em chamadas de função e literais (PEP 448)

```python
def soma(a, b, c):
    return a + b + c

args = (1, 2, 3)
soma(*args)  # equivale a soma(1, 2, 3)

# PEP 448: * múltiplos em literais de lista/tupla/set
merged = [*[1, 2, 3], *[4, 5], 6]        # [1, 2, 3, 4, 5, 6]

# ** para dicionários
merged_dict = {**{"a": 1}, **{"b": 2}, "c": 3}   # {"a": 1, "b": 2, "c": 3}
```

> Antes da PEP 448 (Python 3.5+), `*` só era válido em chamadas de função. Agora pode aparecer múltiplas vezes em literais de sequência e mapeamento.

### 2.5.4 Desempacotamento aninhado

Python permite desempacotar estruturas aninhadas combinando parênteses na atribuição. Casos de uso realmente úteis são raros; o exemplo clássico do livro é extrair apenas o primeiro resultado de uma query SQL que retorna linhas com múltiplas colunas:

```python
query_result = [("Tokyo", "JP", 37_400_000)]
[(city, _, pop)] = query_result
```

```python
metro_areas = [
    ("Tokyo",     "JP", 36.933, (35.689722,  139.691667)),
    ("São Paulo", "BR", 19.649, (-23.547778, -46.635833)),
]

for name, _, _, (lat, lon) in metro_areas:
    if lon <= 0:
        print(f"{name}: {lat:.4f}N, {lon:.4f}W")
```

> Prefira desempacotamento aninhado apenas quando a estrutura dos dados for bem conhecida e a legibilidade ganhar claramente com isso.

---

## 2.6 Pattern Matching com Sequências

### 2.6.1 Por que isso existe?

Antes do Python 3.10, para inspecionar a *forma* de um dado (quantos itens tem, quais tipos, valores específicos) era comum encadear `isinstance`, `len()` e índices manualmente:

```python
if isinstance(comando, list) and len(comando) == 2 and comando[0] == "go":
    direction = comando[1]
    ...
```

O `match/case` substitui esse tipo de verificação por uma sintaxe declarativa: você descreve a *forma esperada* dos dados, e o Python cuida de checar tipo, tamanho e valores de uma vez.

```python
match comando:
    case ["go", direction]:
        ...
```

> Pense no `match` como um `switch` turbinado: em vez de comparar só um valor, ele compara a **estrutura inteira**.

### 2.6.2 Anatomia de um `case`

```python
match sujeito:
    case padrão_1:
        ...
    case padrão_2:
        ...
    case _:
        ...  # coringa, tipo "else"
```

O Python testa os `case`s **na ordem em que aparecem** e executa o primeiro que casar. Se nenhum casar e não houver `_`, nada acontece (sem erro).

### 2.6.3 Casando pelo tamanho da sequência

O caso mais simples: o padrão só declara quantos itens espera.

```python
match ponto:
    case []:
        print("Vazio")
    case [x]:
        print(f"Um item: {x}")
    case [x, y]:
        print(f"Dois itens: {x}, {y}")
    case _:
        print("Três ou mais itens")
```

> **Regra de ouro:** o número de elementos entre colchetes precisa bater exatamente com o tamanho da sequência recebida, a menos que você use `*` (ver 2.6.5).

⚠️ **Pegadinha importante:** embora `str` seja tecnicamente uma sequência de caracteres, o Python **trata `str`, `bytes` e `bytearray` como caso especial** e não deixa elas casarem com padrões de sequência (`case [a, b]`). Isso evita um bug clássico: se não fosse por essa exceção, `match "ab"` cairia em `case [a, b]` como se "ab" fosse uma lista `['a', 'b']`, provavelmente não é isso que se quer.

### 2.6.4 Casando por valor (literal) vs. capturando (variável)

Dentro do padrão, cada posição pode ser:

| Tipo de padrão | Exemplo | O que faz |
|---|---|---|
| Literal | `case [200]` | Só casa se o valor for exatamente `200` |
| Captura | `case [x]` | Casa **qualquer** valor e guarda em `x` |
| Curinga | `case [_, _]` | Casa qualquer coisa, sem guardar nada |

```python
match resposta_http:
    case [200]:
        print("Sucesso")
    case [status]:
        print(f"Outro status: {status}")
```

> Cuidado: `status` na segunda linha não compara com nada, é uma variável nova sendo criada. Para comparar com um valor já existente (ex.: uma constante `OK = 200`), é preciso um literal qualificado (`case [http.OK]`), porque nomes soltos em um padrão são sempre interpretados como captura, nunca como comparação.

### 2.6.5 Capturando "o resto" com `*`

Igual ao desempacotamento (seção 2.5), o `*` recolhe itens excedentes em uma lista:

```python
match linha.split():
    case [primeiro, *meio, ultimo]:
        print(f"Primeiro: {primeiro}, meio: {meio}, último: {ultimo}")
    case [único]:
        print(f"Só um item: {único}")
```

> Isso permite casar sequências de **tamanho variável**, algo que 2.6.3 (tamanho fixo) não permite.

### 2.6.6 Padrões de tipo

Às vezes o objetivo é capturar um valor **só se ele for de um tipo específico**. A sintaxe parece uma chamada de construtor, mas é um padrão:

```python
match ponto:
    case [str(nome), _, _, (float(lat), float(lon))]:
        print(f"{nome}: {lat}, {lon}")
```

> `str(nome)` aqui **não executa** `str()`. É um padrão que diz: "se esse item for uma instância de `str`, capture em `nome`", equivalente a um `isinstance` embutido no padrão.

Isso também combina com **desempacotamento aninhado** (2.5.4): `(float(lat), float(lon))` é um padrão dentro de outro padrão, casando uma tupla de coordenadas.

### 2.6.7 Refinando com guard clauses (`if`)

Quando a estrutura por si só não é suficiente, adiciona-se uma condição extra depois do padrão:

```python
match ponto:
    case [x, y] if x == y:
        print("Está na diagonal")
    case [x, y]:
        print("Fora da diagonal")
```

> A ordem importa: primeiro o Python confere se a **forma** casa (`[x, y]`); só depois avalia o `if`. Se a condição for falsa, ele não desiste do `match` inteiro, apenas passa para o próximo `case`, como se aquele não tivesse casado.

### 2.6.8 Combinando alternativas com `|` e nomeando com `as`

```python
match direcao:
    case ["norte" | "sul" | "leste" | "oeste"] as valida:
        print(f"Direção cardeal: {valida}")
    case _:
        print("Direção inválida")
```

- `|` funciona como "ou" dentro do padrão: qualquer uma das opções casa.
- `as` guarda o **valor inteiro que casou**, útil quando o padrão descreve uma estrutura composta e o objeto original importa, não só suas partes.

### 2.6.9 Exemplo completo do livro

```python
for record in metro_areas:
    match record:
        case [name, _, _, (lat, lon)] if lon <= 0:
            print(f"{name:15} | {lat:9.4f} | {lon:9.4f}")
```

Decompondo:

1. `[name, _, _, (lat, lon)]` espera uma sequência de 4 itens, ignora os dois do meio e desempacota o último como uma tupla de coordenadas (2.6.3 + desempacotamento aninhado).
2. `if lon <= 0` é a guard clause que filtra só o hemisfério oeste (2.6.7).
3. Se o padrão **e** a guarda casarem, o corpo do `case` roda; senão, o laço `for` segue para o próximo `record` sem erro.

Versão executável em [`_04_pattern_matching.py: pattern_matching_metro_areas`](../code/chapter_02/_04_pattern_matching.py).

### 2.6.10 Resumo mental

| Você quer... | Use |
|---|---|
| Casar por tamanho exato | `[a, b, c]` |
| Casar tamanho variável | `[a, *resto]` |
| Ignorar um valor | `_` |
| Checar o tipo de um item | `str(x)`, `int(x)`, etc. |
| Condição extra | `case [...] if condição` |
| Várias opções no mesmo case | `case [a] \| [b]` |
| Guardar o valor todo | `as nome` |

---

## 2.7 Fatiamento

### 2.7.1 O problema que o fatiamento resolve

Pegar "os 3 primeiros itens", "tudo menos o último" ou "um item a cada dois" na mão, com laços e índices, é chato e propenso a erro. O fatiamento (*slicing*) é a ferramenta do Python para extrair pedaços de qualquer sequência de forma direta.

```python
l = [10, 20, 30, 40, 50]

primeiros_tres = l[:3]  # em vez de um for acumulando l[i] em range(3)
```

### 2.7.2 Por que os índices "não incluem o fim"

Pense nos índices não como "rótulos dos itens", mas como **marcadores entre os itens**, como se fossem as marcas de uma régua:

```
    0     1     2     3     4     5
    |  10 |  20 |  30 |  40 |  50 |
```

Cada número marca uma **posição entre elementos**, não o elemento em si. `l[1:3]` significa "corte da marca 1 até a marca 3":

```
    0     1     2     3     4     5
    |  10 [  20 |  30 ]  40 |  50 |
              ↑           ↑
           início=1     fim=3
```

Resultado: `[20, 30]`, os dois itens que ficam **entre** as marcas 1 e 3.

> Pense assim: `l[a:b]` é "tudo que está estritamente entre a marca `a` e a marca `b`". É por isso que o intervalo é **half-open** (meio-aberto): inclui o início, exclui o fim.

Por que essa convenção existe, e por que ela é boa:

1. **Tamanho = subtração direta.** `len(l[1:3])` é `3 - 1 = 2`. Sem essa convenção seria preciso somar 1 sempre.
2. **Fatiar em pedaços não deixa buracos nem sobreposição.** Cortando no ponto `n`, as duas metades se encaixam perfeitamente de volta: `l[:3] + l[3:] == l` para qualquer valor de `3`.
3. **Fácil ver quantos itens tem sem calcular nada**, quando o início é 0: `l[:3]` tem exatamente 3 itens, o número na fatia já é a contagem.

### 2.7.3 Os três parâmetros: `s[início:fim:passo]`

| Parâmetro | O que faz | Se você omitir |
|---|---|---|
| `início` | onde a fatia começa (inclusivo) | `0` (o começo da sequência) |
| `fim` | onde a fatia termina (exclusivo) | `len(s)` (o fim da sequência) |
| `passo` | de quantos em quantos pega os itens | `1` (pega todos, em sequência) |

```python
s = "bicicleta"

s[2:]      # 'cicleta'   -- do índice 2 até o fim
s[:2]      # 'bi'        -- do começo até o índice 2
s[2:5]     # 'cic'       -- entre os índices 2 e 5
s[:]       # 'bicicleta' -- fatia completa (cópia da sequência inteira)

s[::2]     # 'bccea'   -- pega 1, pula 1, pega 1, pula 1...
s[1::2]    # 'iilt'    -- começa no índice 1, de 2 em 2
```

> Truque para não errar: leia `s[início:fim:passo]` em voz alta como "começando em ___, parando antes de ___, pulando de ___ em ___".

### 2.7.4 Índices negativos: contando a partir do fim

Índices negativos contam de trás para frente, onde `-1` é o último item:

```
   -5    -4    -3    -2    -1
    |  10 |  20 |  30 |  40 |  50 |
    0     1     2     3     4     5
```

Cada posição tem dois nomes possíveis, um positivo e um negativo; use o que for mais conveniente para o que você quer expressar:

```python
l[-1]      # 50         -- último item
l[-3:]     # [30,40,50] -- "os últimos 3", sem precisar calcular len(l)-3
l[:-1]     # [10,20,30,40] -- tudo, menos o último
l[1:-1]    # [20,30,40] -- tudo, menos o primeiro e o último
```

> Sempre que pensar "os últimos N itens" ou "tudo menos o último", pense em índice negativo antes de calcular `len()` manualmente. É mais legível e menos propenso a erro de contagem.

### 2.7.5 Passo negativo: percorrendo de trás para frente

Quando o `passo` é negativo, o Python percorre a sequência na direção contrária, e por isso `início` deve ser maior (mais "à direita") que `fim`:

```python
s = "bicicleta"

s[::-1]      # 'atelciciba'  -- toda a string, invertida
s[::-2]      # 'aelcb'       -- invertida, pulando de 2 em 2
s[5:1:-1]    # 'cici'        -- do índice 5 até (sem incluir) o índice 1, de trás pra frente
```

> ⚠️ **Pegadinha:** com passo negativo, `fim` continua sendo exclusivo, mas agora significa "para antes de chegar nesse índice, andando para trás". Inverter `início` e `fim` por engano (`s[1:5:-1]`) resulta numa sequência **vazia**, porque não há caminho válido andando para trás de 1 até 5.

### 2.7.6 O objeto `slice`

`s[a:b:c]` não é uma sintaxe mágica: é açúcar sintático para criar um objeto `slice` e passá-lo para `__getitem__`.

```python
s[1:3]
# equivale a:
s.__getitem__(slice(1, 3))
```

Esse objeto pode ser criado separadamente e reutilizado. Quando se trabalha com dados de largura fixa (extrato bancário, arquivo de layout fixo, colunas de texto alinhadas), dar **nome** às fatias deixa o código muito mais legível:

```python
SKU = slice(0, 6)
DESCRIPTION = slice(6, 40)
UNIT_PRICE = slice(40, 52)

for linha in linhas:
    print(linha[UNIT_PRICE].strip(), linha[DESCRIPTION].strip())
```

Compare com números "mágicos" espalhados sem contexto: `linha[40:52]`, `linha[6:40]`. Demonstração completa com o exemplo do extrato de compras em [`_05_fatiamento.py: fatias_nomeadas_invoice`](../code/chapter_02/_05_fatiamento.py).

> Sempre que a mesma fatia for usada em mais de um lugar do código, ou quando os números não são óbvios à primeira vista, nomeie a fatia com `slice(...)`. É o mesmo princípio de usar uma constante nomeada em vez de um número mágico.

### 2.7.7 Fatiamento com múltiplas dimensões: `a[i, j]`

Quem já usou NumPy ou pandas já viu essa sintaxe:

```python
a[i, j]         # dois índices separados por vírgula
a[m:n, k:l]     # duas fatias separadas por vírgula
```

Por trás, a vírgula dentro dos colchetes cria uma **tupla**, passada de uma vez para `__getitem__`:

```python
a[m:n, k:l]
# equivale a:
a.__getitem__((slice(m, n), slice(k, l)))
```

> ⚠️ Isso **não funciona** com `list`, `tuple` ou `str` do Python puro: essas sequências não sabem o que fazer com uma tupla de índices e lançam `TypeError`. O recurso só funciona em tipos que **implementam explicitamente** esse comportamento em seu `__getitem__`, como `numpy.ndarray` (ver Capítulo 12 para implementar isso em uma classe própria).

### 2.7.8 Atribuindo a uma fatia

Ao **escrever** numa fatia de uma sequência mutável, o lado direito não precisa ter o mesmo tamanho da fatia:

```python
l = list(range(10))
l[2:5] = [20, 30]      # substitui 3 itens por 2: a lista encolhe
l[2:5] = [100]         # substitui 3 itens por 1: encolhe de novo
del l[5:7]             # apaga um trecho
```

Demonstração passo a passo em [`_05_fatiamento.py: atribuindo_a_uma_fatia`](../code/chapter_02/_05_fatiamento.py).

> ⚠️ **Pegadinha clássica:** o lado direito precisa ser um **iterável**, mesmo para colocar um único valor no lugar de vários. Esquecer os colchetes é um erro comum: `l[2:3] = 100` lança `TypeError`; `l[2:3] = [100]` funciona, mesmo trocando 1 item por 1 item.

### 2.7.9 Erros comuns

| Erro | Por que acontece | Como evitar |
|---|---|---|
| `l[3:1]` retorna vazio | Passo positivo (padrão `1`) não anda "para trás" | Use passo negativo: `l[3:1:-1]`, ou inverta início/fim |
| `l[2:3] = 100` dá erro | Lado direito precisa ser iterável | Use `l[2:3] = [100]` |
| Achar que `s[a:b]` tem `b` itens | Confundir índice final com contagem | Lembre: tamanho = `b - a` (quando `a` e `b` são positivos) |
| `a[i, j]` falha em lista comum | Só tipos que implementam `__getitem__` com tupla suportam isso | Funciona em NumPy, não em `list`/`tuple` puros |

### 2.7.10 Síntese

| Você quer... | Use |
|---|---|
| Pegar um pedaço específico | `s[a:b]` |
| Pegar de N em N | `s[a:b:N]` |
| Pegar os últimos N itens | `s[-N:]` |
| Tudo, menos o último | `s[:-1]` |
| Inverter a sequência | `s[::-1]` |
| Reaproveitar a mesma fatia em vários lugares | `nome = slice(a, b)` |
| Trocar um trecho por outro (tamanho pode mudar) | `s[a:b] = novo_iteravel` |
| Apagar um trecho | `del s[a:b]` |

---

## 2.8 Usando `+` e `*` com sequências

### 2.8.1 O comportamento seguro por trás de `+` e `*`

Tanto `+` quanto `*` **sempre criam uma sequência nova**. Nunca modificam as sequências originais:

```python
l = [1, 2, 3]
l2 = l + [4, 5]     # lista NOVA
l3 = l * 3          # lista NOVA
l                   # [1, 2, 3] -- l não mudou
```

Isso funciona da mesma forma para qualquer tipo de sequência:

```python
[1, 2, 3] + [4, 5]      # [1, 2, 3, 4, 5]
(1, 2) + (3, 4)         # (1, 2, 3, 4)
'ab' + 'cd'             # 'abcd'

'abcd' * 3              # 'abcdabcdabcd'
(1, 2) * 3              # (1, 2, 1, 2, 1, 2)
```

> **Regra importante:** `+` só concatena sequências **do mesmo tipo**. `[1, 2] + (3, 4)` lança `TypeError`; é preciso converter uma delas primeiro (`[1, 2] + list((3, 4))`).

### 2.8.2 O que `*` realmente faz

`sequência * n` é, na prática, um atalho para concatenar a sequência com ela mesma `n` vezes: `l * 3` equivale a `l + l + l`.

Para tipos imutáveis (números, strings, tuplas de imutáveis), isso é seguro, porque não há risco de "compartilhar" um item entre as cópias: um item imutável nunca muda, então tanto faz se é "o mesmo objeto" repetido ou cópias distintas.

```python
5 * 'x'          # 'xxxxx' -- sem problema, string é imutável
(0,) * 5         # (0, 0, 0, 0, 0) -- sem problema, int é imutável
```

### 2.8.3 A pegadinha clássica: `*` com itens **mutáveis**

Este é o bug mais comum envolvendo esse operador. Um "tabuleiro" 3×3, lista de listas:

```python
board = [['_'] * 3] * 3
```

```
[['_', '_', '_'],
 ['_', '_', '_'],
 ['_', '_', '_']]
```

Parece correto. Mas alterar **uma única posição** revela o problema:

```python
board[1][2] = 'X'
```

```
[['_', '_', 'X'],
 ['_', '_', 'X'],
 ['_', '_', 'X']]
```

As três linhas mudaram, apesar de só a linha 1 ter sido alterada. Demonstração em [`_06_operadores.py: board_bug_referencia_compartilhada`](../code/chapter_02/_06_operadores.py).

**Por que isso acontece:** listas armazenam referências, não os valores em si (o mesmo princípio de 2.4.4, tuplas com itens mutáveis). `[['_'] * 3] * 3` acontece em duas etapas:

1. `['_'] * 3` cria **uma** lista interna: `['_', '_', '_']`. Chame-a de `linha`.
2. `[linha] * 3` cria uma lista externa com **três referências para essa mesma `linha`**, não três listas diferentes:

```
board = [ →linha, →linha, →linha ]
              ↓        ↓        ↓
           ['_','_','_']  (é o MESMO objeto, apontado 3 vezes)
```

Por isso, `board[1][2] = 'X'` modifica **o único objeto `linha` que existe**; como as três posições de `board` apontam para ele, as três "parecem" mudar ao mesmo tempo.

> Multiplicar uma sequência não faz **cópias profundas** dos itens, só duplica as **referências**. Se o item é imutável (como `'_'`), isso é invisível e inofensivo. Se o item é mutável (como uma lista), o compartilhamento vira um bug.

### 2.8.4 A forma correta: usando uma list comprehension

O truque para gerar linhas realmente independentes é usar um `for`, que executa a expressão **uma vez por iteração**, criando um objeto novo a cada passagem:

```python
board = [['_'] * 3 for i in range(3)]
board[1][2] = 'X'
```

```
[['_', '_', '_'],
 ['_', '_', 'X'],
 ['_', '_', '_']]
```

Agora só a linha certa mudou. Ver [`_06_operadores.py: board_correto_com_listcomp`](../code/chapter_02/_06_operadores.py).

| Código | O que acontece |
|---|---|
| `[['_']*3] * 3` | Cria a linha **uma vez**, repete a **referência** 3 vezes |
| `[['_']*3 for i in range(3)]` | Executa `['_']*3` **três vezes**, criando 3 listas de fato distintas |

> **Regra prática:** ao criar uma estrutura aninhada e mutável (lista de listas, lista de dicionários etc.) repetida N vezes, desconfie de `[x] * n`. Prefira `[x for _ in range(n)]`, mesmo que `x` pareça simples.

### 2.8.5 `+=` e `*=` não fazem sempre a mesma coisa

`+=` parece uma única operação, mas o que acontece por baixo dos panos depende de **quem está do lado esquerdo**:

| Situação | O que `+=` faz | Método especial |
|---|---|---|
| Sequência **mutável** (`list`) | Modifica **no próprio lugar** (mesmo objeto, mesmo `id`) | `__iadd__` |
| Sequência **imutável** (`tuple`, `str`) | Cria um objeto **novo** e reatribui a variável | Cai no `__add__` |

Quando o objeto tem `__iadd__` implementado (como `list`), o Python o usa para alterar a sequência existente: é mais eficiente, porque não precisa realocar memória para uma cópia inteira. Quando o objeto não tem `__iadd__` (como `tuple`), o Python cai no comportamento padrão, `a = a + b`, que sempre gera um objeto novo. Verificação com `id()` em [`_06_operadores.py: iadd_lista_vs_tupla`](../code/chapter_02/_06_operadores.py).

> **Consequência prática de desempenho:** fazer `+=` repetidamente numa tupla dentro de um loop é bem mais custoso do que numa lista, porque cada `+=` aloca uma tupla inteiramente nova. Uma lista cresce no lugar; uma tupla recria o objeto inteiro a cada iteração.

### 2.8.6 O caso mais estranho: `+=` num item mutável dentro de uma tupla

```python
t = (1, 2, [30, 40])
t[2] += [50, 60]
```

O resultado é **duas coisas ao mesmo tempo**: `TypeError: 'tuple' object does not support item assignment`, mas checando `t` depois do erro:

```python
t   # (1, 2, [30, 40, 50, 60])
```

A lista interna **foi alterada**, mesmo com o erro tendo sido lançado. Isso faz sentido ao entender os dois passos que `t[2] += [50, 60]` executa por trás dos panos:

1. **Primeiro**, o Python calcula `t[2].__iadd__([50, 60])`. Como `t[2]` é uma **lista** (mutável), esse passo funciona: a lista é alterada no próprio lugar, virando `[30, 40, 50, 60]`.
2. **Depois**, o Python tenta fazer `t[2] = <resultado do passo 1>`, reatribuindo a posição 2 da tupla. Tuplas não aceitam atribuição por índice, e é aí que o `TypeError` estoura.

O efeito colateral do passo 1 já ficou registrado antes do passo 2 falhar. Reprodução em [`_06_operadores.py: iadd_em_item_mutavel_dentro_de_tupla`](../code/chapter_02/_06_operadores.py).

> ⚠️ **Lição prática:** evite guardar objetos mutáveis (listas, dicts, sets) dentro de tuplas. Se precisar fazer isso, nunca use `+=` (ou qualquer atribuição aumentada) diretamente num item da tupla, mesmo que "às vezes pareça funcionar".

### 2.8.7 Síntese

| Você quer... | Cuidado |
|---|---|
| Concatenar duas sequências | `a + b`, precisam ser do mesmo tipo |
| Repetir uma sequência de **imutáveis** | `s * n`, seguro |
| Repetir uma sequência de **mutáveis** (listas dentro de listas) | não use `[x] * n`; use `[x for _ in range(n)]` |
| Acrescentar itens numa lista existente | `l += outra`, modifica no lugar, rápido |
| Acrescentar itens numa tupla | `t += outra`, cria tupla nova, mais custoso |
| Alterar item mutável dentro de uma tupla | evite: pode dar erro mesmo alterando o conteúdo |

---

## 2.9 `list.sort()` vs `sorted()`

### 2.9.1 Ordenar "no lugar" ou criar uma cópia ordenada?

Python oferece **duas** formas de ordenar uma sequência, e a escolha entre elas depende de uma pergunta simples: você quer preservar a sequência original?

```python
frutas = ['morango', 'abacaxi', 'banana']

nova = sorted(frutas)   # não mexe no original
frutas.sort()           # modifica no próprio lugar
```

> **Regra de memória:** o nome já entrega a diferença. `sorted(x)` é uma **função** que recebe qualquer iterável e **devolve** uma lista nova, sem tocar em `x`. `x.sort()` é um **método** que só existe em `list` e ordena a própria lista **no lugar**, sem devolver nada de útil.

### 2.9.2 A pegadinha nº 1: `sort()` devolve `None`

A confusão mais comum entre iniciantes:

```python
frutas = ['morango', 'abacaxi', 'banana']
frutas = frutas.sort()   # ⚠️ ARMADILHA
print(frutas)            # None
```

`frutas.sort()` ordenou a lista original com sucesso, mas o valor de retorno do método é `None`. Ao escrever `frutas = frutas.sort()`, a lista ordenada é descartada e `frutas` passa a ser `None`. Ver [`_07_ordenacao.py: sort_devolve_none`](../code/chapter_02/_07_ordenacao.py).

> Essa é uma convenção proposital em Python: **funções/métodos que alteram um objeto no lugar devolvem `None`**, para deixar claro que eles não devem ser encadeados como se produzissem um valor novo. O mesmo padrão aparece em `list.reverse()`, `list.append()`, `dict.update()`, etc.

Forma correta:

```python
frutas.sort()          # não reatribua
print(frutas)          # ['abacaxi', 'banana', 'morango']
```

### 2.9.3 Quando usar cada um

| Situação | Use |
|---|---|
| Só a lista precisa existir ordenada, sem necessidade da versão original | `l.sort()`, mais eficiente, não gasta memória com uma cópia |
| A sequência original precisa ser mantida **e** também uma versão ordenada | `sorted(l)` |
| A entrada não é uma `list` (tupla, `range`, gerador, string...) | `sorted(x)`, `sort()` só existe em `list` |

```python
t = (3, 1, 2)
t.sort()          # AttributeError: 'tuple' object has no attribute 'sort'

sorted(t)          # [1, 2, 3] -- sorted() aceita qualquer iterável e devolve list
sorted('bda')      # ['a', 'b', 'd'] -- funciona até com string
```

> `sorted()` **sempre devolve uma `list`**, independentemente do tipo do iterável de entrada. Para o resultado como string, é preciso recompor: `''.join(sorted('bda'))`.

### 2.9.4 Os parâmetros em comum: `reverse` e `key`

Tanto `sort()` quanto `sorted()` aceitam os **mesmos dois parâmetros nomeados**, com o mesmo comportamento nos dois casos.

**`reverse`** inverte a ordem da comparação:

```python
sorted([5, 1, 4, 2, 3], reverse=True)    # [5, 4, 3, 2, 1]
```

> ⚠️ **Pegadinha comum:** `reverse=True` não significa "ordena e depois inverte o resultado" (embora o efeito final pareça igual em muitos casos), significa "ordena usando o critério de comparação invertido". Isso importa quando há empates: itens iguais mantêm a ordem relativa original mesmo com `reverse=True` (ver 2.9.5).

**`key`** muda **o critério** usado para comparar, sem mudar os itens. É o parâmetro mais poderoso dos dois: recebe uma função aplicada a **cada item** antes da comparação, mas o item original (não transformado) é o que aparece no resultado:

```python
palavras = ['banana', 'Abacaxi', 'uva', 'Kiwi']

sorted(palavras)               # ['Abacaxi', 'Kiwi', 'banana', 'uva'] -- maiúsculas antes de minúsculas na tabela ASCII
sorted(palavras, key=str.lower)  # ['Abacaxi', 'banana', 'Kiwi', 'uva'] -- compara em minúsculo, devolve original
sorted(palavras, key=len)        # ['uva', 'Kiwi', 'banana', 'Abacaxi']
```

> Imagine que o Python cria, só para fins de comparação, uma "lista invisível" com `key(item)` aplicado a cada elemento, e ordena com base nela. O que volta no resultado são sempre os itens **originais**, na nova ordem.

### 2.9.5 Por que a ordenação em Python é estável

O algoritmo de ordenação do Python (Timsort) é **estável**: se dois itens são "iguais" segundo o critério de comparação, a ordem relativa entre eles não muda.

```python
alunos = [("Ana", 8.5), ("Bruno", 7.0), ("Carla", 8.5), ("Davi", 7.0)]
sorted(alunos, key=lambda a: a[1])
# [('Bruno', 7.0), ('Davi', 7.0), ('Ana', 8.5), ('Carla', 8.5)]
```

Bruno continua antes de Davi (ambos com nota 7.0), e Ana continua antes de Carla (ambos com 8.5): a ordem original entre empates foi preservada. Ver [`_07_ordenacao.py: sorted_e_estavel`](../code/chapter_02/_07_ordenacao.py).

> Estabilidade permite ordenar por **múltiplos critérios em etapas**, do menos importante para o mais importante: primeiro por nome (critério secundário), depois o resultado por nota (critério principal); em caso de empate na nota, a ordem alfabética é preservada.

### 2.9.6 Uma pegadinha de desempenho: `key` roda uma vez por item

`key` é preferível a passar uma função de comparação direta (existia no Python 2, removido no Python 3) porque a função passada em `key` é executada **uma única vez para cada item**, e o resultado fica guardado para todas as comparações seguintes: `key(item)` é chamada exatamente `n` vezes (uma por item), não uma vez por comparação.

> Mesmo que `key` seja uma função "cara" (cálculo pesado), ela não vira um gargalo proporcional ao número de comparações, só ao número de itens.

### 2.9.7 Síntese

| Você quer... | Use |
|---|---|
| Ordenar uma lista sem precisar mais da versão original | `lista.sort()` |
| Manter o original intacto e obter uma cópia ordenada | `sorted(iteravel)` |
| Ordenar algo que não é `list` (tupla, string, gerador...) | `sorted(iteravel)`, `sort()` não existe fora de `list` |
| Ordem decrescente | `reverse=True` (nos dois) |
| Ordenar por um critério diferente do valor "cru" | `key=funcao` (nos dois) |
| Ordenar por múltiplos critérios | Aplique `sorted()` em etapas, do menos para o mais importante, aproveitando a estabilidade |

---

## 2.10 Quando uma Lista Não é a Resposta

### 2.10.1 O problema: `list` é ótima, mas nem sempre é a ferramenta certa

`list` foi a sequência-padrão usada em quase todos os exemplos até aqui. Ela é flexível e fácil de usar, mas essa mesma flexibilidade, em alguns cenários, vira desperdício:

- Guardando só **números**, gastar memória com *referências* para objetos `int`/`float` espalhados pela memória, em vez dos valores em si, é desperdício.
- Se as operações são só **inserção e remoção nas pontas** (início e fim), uma estrutura otimizada para acesso aleatório no meio é a ferramenta errada.

Esta seção apresenta alternativas à `list` para esses casos específicos: `array`, `memoryview`, NumPy e `deque`.

### 2.10.2 `array`: quando você só guarda números

Sequências **contêiner** vs. **planas** (seção 2.2): `list` é contêiner, guarda ponteiros para objetos `int`/`float` espalhados na memória. Uma lista com 1 milhão de números significa 1 milhão de objetos Python soltos por aí, cada um com seu próprio cabeçalho de metadados (`ob_refcnt`, `ob_type`...).

```
list de floats:          array de floats:
[ →3.14, →2.71, →1.41 ]  [ 3.14 | 2.71 | 1.41 ]
    ↓      ↓      ↓        (valores direto, lado a lado, sem indireção)
  objeto objeto objeto
   float  float  float
```

`array.array` é uma sequência **plana**: guarda os valores numéricos crus, em um bloco contíguo de memória, no formato nativo da CPU (como um array em C). Isso economiza memória e acelera operações numéricas.

```python
from array import array
floats = array('d', (random() for i in range(10**7)))
```

> O primeiro argumento, `'d'`, é o **typecode**: define o tipo C usado para armazenar cada item (`'d'` = double / float de 64 bits, `'i'` = signed int, `'B'` = unsigned char, etc.). Todo item do array precisa ser do mesmo tipo.

Como o array guarda os bytes crus, salvar e carregar é praticamente uma cópia direta de memória para disco, sem precisar "traduzir" cada número individualmente (demonstração em [`_08_estruturas_especializadas.py: array_grava_e_le_em_disco`](../code/chapter_02/_08_estruturas_especializadas.py)). Isso é ordens de magnitude mais rápido do que ler/escrever os mesmos números em um arquivo texto linha por linha, já que não há parsing/formatação, só cópia de bytes.

`array` perde funcionalidades como `sort()`; para ordenar, é preciso reconstruir:

```python
a = array('d', [3.0, 1.0, 2.0])
a = array(a.typecode, sorted(a))
```

### 2.10.3 `memoryview`: enxergando os bytes de dentro de outra estrutura, sem copiar

Um `array` de 1 milhão de itens, quando só é preciso ler ou modificar um pedacinho dele: `array[100:200]` **copia** esses 100 itens para uma nova estrutura, desperdício de memória e tempo para um uso temporário.

`memoryview` permite **compartilhar a memória** de uma sequência sem copiá-la, funcionando como uma "janela" para os bytes de dentro do objeto original:

```python
import array
numeros = array.array('h', [-2, -1, 0, 1, 2])   # 'h' = short int
memv = memoryview(numeros)
```

Uma aplicação poderosa: "trocar as lentes" e enxergar os mesmos bytes crus como se fossem de outro tipo, sem copiar nada. Alterar a view altera o array original, porque é a mesma região de memória. Demonstração completa em [`_08_estruturas_especializadas.py: memoryview_sobre_array`](../code/chapter_02/_08_estruturas_especializadas.py).

> ⚠️ Mudar **um único byte** pode mudar o valor de um inteiro inteiro (cada `short` ocupa 2 bytes). `memoryview` dá esse tipo de controle de baixo nível, útil para processamento de imagens, áudio, protocolos binários, etc.

### 2.10.4 NumPy: trocando laços `for` por operações vetorizadas

Um laço `for` em Python processa **um item por vez**, e cada iteração carrega o custo do interpretador (verificação de tipos, chamadas de método etc.). Para milhões de números isso é lento, não porque o laço em si seja ruim, mas porque o Python não foi feito para esse tipo de repetição massiva.

NumPy resolve isso com **vetorização**: a operação é aplicada na estrutura **inteira** de uma vez, e o cálculo real acontece em código C compilado, não em bytecode Python interpretado item a item.

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])
soma = a + b   # array([11, 22, 33, 44, 55])
```

> `+` **não** concatena os arrays (como faria com listas): o NumPy sobrescreve os operadores para significar "some elemento a elemento". Isso é possível porque `ndarray` implementa seus próprios `__add__`, `__mul__` etc.

Indexação booleana é o equivalente vetorizado de um `if` dentro de uma comprehension:

```python
numeros = np.arange(20)
mascara = (numeros > 10) & (numeros % 2 == 0)   # array de True/False
numeros[mascara]                                  # array([12, 14, 16, 18])
```

E o fatiamento multidimensional (seção 2.7.7, `a[i, j]`) aparece de novo para separar colunas antes de uma operação, como uma distância euclidiana:

```python
pontos = np.array([(1, 2), (3, 4), (5, 6)])
x, y = pontos[:, 0], pontos[:, 1]     # todas as linhas, coluna 0 e coluna 1
distancias = np.sqrt(x**2 + y**2)
```

Todos os exemplos vetorizados, com a versão equivalente em `for`, estão em [`code/chapter_02/`](../code/chapter_02/) (`numpy_soma_vetorizada`, `numpy_quadrado_vetorizado`, `numpy_filtro_com_mascara`, `numpy_distancia_euclidiana`).

| Aspecto | Laço `for` | Operação vetorizada |
|---|---|---|
| Onde o cálculo roda | Interpretador Python, item a item | Código C compilado, em bloco |
| Overhead por item | Alto (bytecode, checagem de tipo a cada iteração) | Praticamente zero |
| Uso de memória | Cria objetos Python intermediários | Usa buffers contíguos de baixo nível |
| Escala para milhões de itens | Degradação perceptível | Diferença de ordens de magnitude |

> Vetorização não é só "mais rápido por rapidez": é uma mudança de como o problema é pensado. Em vez de descrever o que fazer com "um item de cada vez", descreve-se uma operação sobre a coleção **inteira**.

### 2.10.5 `deque`: quando você mexe nas duas pontas o tempo todo

Para entender por que `deque` é rápida, primeiro é preciso entender **por que `list` é lenta** em certas operações, e isso tem a ver com como cada uma é organizada na memória.

Uma `list` é implementada como um **array dinâmico**: um bloco **único e contíguo** de memória, com cada posição "colada" na seguinte.

```
list:  [ 10 | 20 | 30 | 40 ]
         ↑ posições fixas, uma coladinha na outra
```

`list.insert(0, 5)` (inserir no início) não encontra "espaço vazio" esperando na posição 0: o Python precisa **fisicamente deslocar** todos os outros itens uma casa para a direita, para abrir espaço:

```
antes:    [ 10 | 20 | 30 | 40 ]
insert(0, 5):
             10→  20→  30→  40→   (todos se movem 1 posição)
depois:   [  5 | 10 | 20 | 30 | 40 ]
```

Quanto mais itens existem depois da posição 0, mais cópias de memória são necessárias, o custo cresce proporcionalmente ao tamanho da lista (`O(n)`). `append()` no final é rápido (`O(1)` na maioria das vezes), porque não precisa mover nada, só "encosta" o novo item depois do último.

`deque` não é um bloco único contíguo: é implementada como uma **sequência de blocos de tamanho fixo, encadeados** (parecido com uma lista duplamente encadeada de blocos). Cada bloco tem um ponteiro para o próximo e para o anterior:

```
deque:  [bloco A] ⇄ [bloco B] ⇄ [bloco C]
         ↑ início                    ↑ fim
```

Como a estrutura já mantém referências diretas para as duas pontas, inserir ou remover ali significa apenas criar (ou liberar) um espaço no bloco da ponta correspondente e atualizar um punhado de ponteiros. Não é necessário mover nenhum outro item, diferente da `list`, onde inserir no início obriga a reorganizar tudo que vem depois. É por isso que `appendleft()` e `append()` custam o mesmo (`O(1)`), não importa se a deque tem 10 ou 10 milhões de itens.

> **A troca que se faz ao usar `deque`:** velocidade nas pontas em troca de acesso ao meio, que fica lento. Acessar `deque[500000]` exige "andar" bloco por bloco a partir de uma das pontas (`O(n)`), enquanto `list[500000]` é instantâneo (`O(1)`), pois uma posição de array contíguo é calculada diretamente (endereço base + índice × tamanho do item).

```python
from collections import deque
dq = deque(range(10), maxlen=10)
dq.rotate(3)    # pega 3 itens do final e recoloca no início
```

> `rotate(n)` positivo pega `n` itens do **final** e recoloca no início; `rotate(-n)` faz o inverso. Isso só é barato porque, internamente, é implementado como uma sequência de `pop`/`appendleft` nas pontas, as mesmas operações `O(1)` de cima, repetidas `n` vezes. Demonstração em [`_08_estruturas_especializadas.py: deque_rotate`](../code/chapter_02/_08_estruturas_especializadas.py).

O recurso mais interessante de `deque` é `maxlen`: ela vira um **buffer circular**, itens antigos são descartados automaticamente conforme novos entram (demonstração em [`_08_estruturas_especializadas.py: deque_buffer_circular`](../code/chapter_02/_08_estruturas_especializadas.py)):

```python
dq = deque([10, 20, 30], maxlen=3)
dq.appendleft(0)     # empurra o 30 para fora, dq = deque([0, 10, 20], maxlen=3)
```

> **Caso de uso clássico:** manter "os últimos N eventos" de um log, ou "o histórico recente" de uma conversa/jogo, sem se preocupar em limpar manualmente os itens antigos.

Remover ou inserir no **meio** de uma `deque` (não nas pontas) é lento, o oposto de `list`, que é rápida no meio (para leitura por índice) mas lenta nas pontas de inserção. A escolha da estrutura depende de **onde** se mexe na sequência:

| Operação | `list` | `deque` | Por quê |
|---|---|---|---|
| Inserir/remover no final | Rápido `O(1)` | Rápido `O(1)` | Nenhuma das duas precisa mover outros itens |
| Inserir/remover no início | Lento `O(n)` | Rápido `O(1)` | `list` precisa deslocar tudo; `deque` só mexe ponteiros |
| Acessar por índice no meio | Rápido `O(1)` | Lento `O(n)` | `list` calcula endereço direto; `deque` precisa "andar" pelos blocos |
| Limitar tamanho automaticamente | não tem | `maxlen` | Recurso nativo de buffer circular |

### 2.10.6 Outras filas mencionadas (visão rápida)

O livro cita brevemente outras estruturas de fila da biblioteca padrão, cada uma para um cenário diferente:

| Estrutura | Quando usar |
|---|---|
| `queue.SimpleQueue` / `Queue` | Filas thread-safe, para comunicação entre threads |
| `multiprocessing.Queue` | Filas entre processos separados |
| `asyncio.Queue` | Filas para código assíncrono (coroutines) |
| `heapq` | Não é uma classe de fila, mas funções para tratar uma `list` comum como uma fila de prioridade (heap) |

> Essas ficam fora do escopo detalhado da seção; o ponto é saber que existem, para quando o cenário pedir concorrência ou prioridade em vez de simples FIFO/LIFO.

### 2.10.7 Síntese: escolhendo a sequência certa

| Você precisa de... | Use |
|---|---|
| Coleção genérica, de qualquer tipo, uso geral | `list` |
| Só números, economia de memória, I/O rápido em disco | `array.array` |
| "Espiar"/editar bytes de outra estrutura sem copiar | `memoryview` |
| Matrizes, computação numérica pesada, operações elemento a elemento sem `for` | `numpy.ndarray` |
| Fila com inserção/remoção rápida nas **duas pontas** | `collections.deque` |
| Histórico limitado ("últimos N itens") | `deque(maxlen=N)` |
| Fila thread-safe / entre processos / assíncrona | `queue.*`, `multiprocessing.Queue`, `asyncio.Queue` |
| Fila de prioridade | `heapq` sobre uma `list` |

---

## Síntese do Capítulo

O fio condutor do capítulo é sempre o mesmo: **referência vs. valor, e no lugar vs. cópia nova**. Boa parte das pegadinhas vistas (2.4.4, 2.8.3, 2.8.6) vêm do mesmo lugar: um contêiner guarda referências, não os objetos em si, e multiplicar ou copiar a estrutura externa não duplica o que está dentro.

- **Sintaxe de construção e desmonte.** Listcomps/genexps (2.3) constroem sequências; `*`/`**` e pattern matching (2.5, 2.6) as desmontam. Ambos os lados aceitam a mesma ideia de "capturar o resto" com `*`.
- **Tuplas como registro vs. lista imutável** (2.4) explicam por que uma tupla pode "mudar" por dentro (2.4.4) e por que ela não deveria guardar itens mutáveis.
- **Fatiamento** (2.7) é a base para o restante do capítulo: a convenção meio-aberta reaparece no fatiamento multidimensional do NumPy (2.10.4) e a ideia de nomear uma fatia com `slice(...)` é a mesma de nomear qualquer constante.
- **`+`, `*`, `+=`, `*=`** (2.8) só são seguros sem ressalvas com itens imutáveis; com mutáveis, a diferença entre "criar `n` referências" e "criar `n` objetos" (`[x] * n` vs. `[x for _ in range(n)]`) é o que separa o código correto do bug clássico do tabuleiro.
- **Ordenação** (2.9) é previsível por dois motivos: a convenção de que mutação no lugar devolve `None`, e a estabilidade do Timsort, que permite compor critérios em etapas.
- **Além da `list`** (2.10): a escolha da estrutura é sempre uma troca explícita, memória por indireção (`array`), cópia por referência (`memoryview`), laço por vetorização (NumPy), acesso ao meio por acesso nas pontas (`deque`). Não existe estrutura universalmente melhor, só a mais adequada ao padrão de uso.

No fim, o capítulo defende uma postura: conhecer bem `list`, `tuple` e o fatiamento cobre a maioria dos casos; as estruturas de 2.10 só valem a complexidade extra quando o perfil de uso (volume de dados, ponta de inserção, necessidade de vetorização) realmente pede por elas.
