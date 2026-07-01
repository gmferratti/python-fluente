# Capítulo 03: Dicionários e Conjuntos

## Resumo Geral

Dicionários não são apenas uma estrutura de dados conveniente em Python: fazem parte da implementação da própria linguagem. Atributos de instância, namespaces de módulos e argumentos nomeados de função são todos representados internamente por dicts. Entender bem `dict` e `set`, portanto, é entender uma parte importante de como o interpretador funciona por baixo do código que escrevemos.

- **3.1** cobre a sintaxe moderna de criação e fusão de dicts: dictcomps, `**` e os operadores `|`/`|=`.
- **3.2** estende `match/case` para mapeamentos, com casamento parcial por chave.
- **3.3** explica por que chaves precisam ser hashable e o padrão `setdefault`.
- **3.4** trata o tratamento automático de chaves ausentes: `defaultdict` e `__missing__`.
- **3.5** apresenta variações de dict da biblioteca padrão: `OrderedDict`, `ChainMap`, `Counter` e `UserDict`.
- **3.6** cobre mapeamentos imutáveis via `types.MappingProxyType`.
- **3.7** explica as views de dicionário (`.keys()`, `.values()`, `.items()`) como projeções, não cópias.
- **3.8** liga esses comportamentos à implementação interna por tabela de hash.
- **3.9** apresenta `set`/`frozenset` e a álgebra de conjuntos como operadores infixos.
- **3.10** mostra que `dict_keys` e `dict_items` já se comportam como conjuntos.

Os exemplos de código mais extensos ou executáveis estão em [`code/chapter_03/`](../code/chapter_03/); aqui ficam apenas os trechos curtos que ilustram um ponto específico do texto.

---

## 3.1 Sintaxe Moderna de Criação e Manipulação de Dicts

### 3.1.1 Compreensões de dict

O mesmo mecanismo das listcomps se aplica a dicionários: uma dictcomp constrói um `dict` a partir de qualquer iterável de pares, em uma única expressão.

```python
dial_codes = [(880, 'Bangladesh'), (55, 'Brazil'), (86, 'China'),
              (91, 'India'), (62, 'Indonesia'), (81, 'Japan')]

country_dial = {country: code for code, country in dial_codes}
```

Vale notar a inversão: a lista original traz `(código, país)`, mas na dictcomp o país é a chave, então a ordem no corpo da expressão se inverte. É comum, ao escrever uma dictcomp, primeiro decidir qual campo faz sentido como chave e só depois montar a expressão.

O mesmo padrão de filtro e transformação das listcomps funciona aqui:

```python
{code: country.upper()
 for country, code in sorted(country_dial.items())
 if code < 70}
```

### 3.1.2 Desempacotamento de mapeamentos com `**`

Desde a PEP 448 (Python 3.5), `**` pode aparecer mais de uma vez em uma chamada de função, contanto que não haja chaves repetidas entre os argumentos:

```python
def dump(**kwargs):
    return kwargs

dump(**{'x': 1}, y=2, **{'z': 3})
# {'x': 1, 'y': 2, 'z': 3}
```

O mesmo `**` também funciona dentro de um literal `dict`, e aqui a regra muda: chaves duplicadas são permitidas, e a última ocorrência prevalece.

```python
{'a': 0, **{'x': 1}, 'y': 2, **{'z': 3, 'x': 4}}
# {'a': 0, 'x': 4, 'y': 2, 'z': 3}
```

> Pense em `**dict` como uma forma de inserir todos os pares de um dicionário dentro de outro no ponto exato em que ele aparece na expressão. Se houver colisão de chaves, o que vier depois sobrescreve o que veio antes, exatamente como aconteceria fazendo as atribuições em sequência.

### 3.1.3 Fusão de dicionários com `|` e `|=`

Desde o Python 3.9, `|` funciona como operador de união também para dicts, o mesmo símbolo usado para união de conjuntos.

```python
d1 = {'a': 1, 'b': 3}
d2 = {'a': 2, 'b': 4, 'c': 6}

d1 | d2   # cria um novo dict: {'a': 2, 'b': 4, 'c': 6}
d1        # continua inalterado: {'a': 1, 'b': 3}

d1 |= d2  # agora sim, modifica d1 no lugar
d1        # {'a': 2, 'b': 4, 'c': 6}
```

> A diferença entre os dois operadores é a mesma que existe entre `+` e `+=` em listas: um cria um objeto novo, o outro altera o existente. Demonstração completa em [`_01_dict_comprehensions.py`](../code/chapter_03/_01_dict_comprehensions.py).

---

## 3.2 Pattern Matching com Mapeamentos

`match/case` também aceita mapeamentos como sujeito, casando com qualquer instância real ou virtual de `collections.abc.Mapping`. A diferença em relação a padrões de sequência (Capítulo 2) é que aqui o casamento é parcial: chaves presentes no sujeito mas não mencionadas no padrão simplesmente não são levadas em conta, e não impedem o match.

```python
def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:
            return names
        case {'type': 'book', 'api': 1, 'author': name}:
            return [name]
        case {'type': 'book'}:
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:
            return [name]
        case _:
            raise ValueError(f'Invalid record: {record!r}')
```

A lógica é de cima para baixo: primeiro testa-se o formato mais recente da API de livros, depois o formato antigo, depois qualquer outro registro de livro que não bateu com os dois anteriores (o que indica um problema), e por fim o formato de filme. O `case _` final captura qualquer coisa que não seja nem livro nem filme.

Um registro com uma chave extra, como `'title'`, continua casando normalmente com o primeiro ou segundo padrão, já que essa chave não é mencionada em nenhum dos dois. Essa flexibilidade é útil ao lidar com dados vindos de JSON ou de bancos de documentos, onde registros costumam ter campos opcionais.

Para capturar as chaves não referenciadas explicitamente, usa-se `**variavel`, que deve ser o último item do padrão:

```python
match food:
    case {'category': 'ice cream', **details}:
        print(details)
```

> Esse casamento consulta o mapeamento por meio de `d.get(key, sentinel)`, então não aciona o comportamento de um `defaultdict` nem o método `__missing__`. A chave precisa já existir no sujeito para que o padrão bata. Versão executável em [`_02_pattern_matching.py`](../code/chapter_03/_02_pattern_matching.py).

---

## 3.3 API Padrão dos Tipos de Mapeamento

O módulo `collections.abc` define `Mapping` e `MutableMapping`, úteis quando o código precisa checar com `isinstance` se um objeto se comporta como mapeamento, sem exigir que seja especificamente um `dict`.

### 3.3.1 Por que chaves precisam ser hashable

Toda chave de dict, e todo elemento de set, precisa ser hashable: precisa ter um código de hash que não muda durante sua vida útil, e precisa suportar comparação de igualdade. Isso não é uma restrição arbitrária: é o que permite ao dict localizar uma entrada em tempo praticamente constante, calculando a posição diretamente a partir do hash em vez de percorrer a estrutura inteira procurando a chave.

```python
tt = (1, 2, (30, 40))              # hashable
tl = (1, 2, [30, 40])              # não hashable, contém uma lista
tf = (1, 2, frozenset([30, 40]))   # hashable, frozenset é hashable
```

> Números, `str` e `bytes` são sempre hashable. Tuplas e `frozenset` são hashable somente se todo o conteúdo interno também for. Listas, dicts e `set` nunca são hashable, justamente por serem mutáveis: se o conteúdo pudesse mudar, o hash também mudaria, e a posição calculada anteriormente na tabela deixaria de fazer sentido.

### 3.3.2 `setdefault`

Um padrão comum é buscar um valor mutável associado a uma chave, criando-o se ainda não existir, e então atualizá-lo. Escrito da forma direta, isso faz até três buscas pela mesma chave:

```python
occurrences = index.get(word, [])
occurrences.append(location)
index[word] = occurrences
```

`setdefault` resolve isso com uma única busca:

```python
index.setdefault(word, []).append(location)
```

A leitura é: pegue o valor associado a `word`, criando-o com o default `[]` se ainda não existir, e devolva esse valor, seja ele o que já estava lá ou o recém-criado. Como o retorno é sempre a lista em questão, dá para encadear `.append()` na mesma linha. Demonstração em [`_03_setdefault.py`](../code/chapter_03/_03_setdefault.py).

---

## 3.4 Tratamento Automático de Chaves Ausentes

A biblioteca padrão oferece duas abordagens para lidar com buscas por chaves inexistentes.

### 3.4.1 `collections.defaultdict`

Um `defaultdict` recebe um invocável, guardado no atributo `default_factory`, que é chamado automaticamente sempre que `__getitem__` (a sintaxe `d[k]`) encontra uma chave ausente.

```python
import collections
index = collections.defaultdict(list)
index[word].append(location)
```

Se `word` ainda não existe, `list()` é chamado para criar a lista vazia, que é armazenada em `index[word]` e devolvida, tudo antes de `.append()` ser executado. O resultado prático é que a linha acima nunca falha por chave ausente, mesmo na primeira vez que uma palavra aparece.

> Esse comportamento só acontece com `d[k]`. Chamar `d.get(k)` para uma chave ausente continua devolvendo `None`, e `k in d` continua devolvendo `False`, sem acionar `default_factory`.

### 3.4.2 O método `__missing__`

`defaultdict` é construído sobre um mecanismo mais geral: o método `__missing__`, que qualquer subclasse de `dict` pode implementar. Quando `__getitem__` não encontra a chave, delega para `__missing__` antes de gerar `KeyError`.

```python
class StrKeyDict0(dict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()
```

O objetivo dessa classe é permitir buscar tanto por `d['13']` quanto por `d[13]`, tratando ambos como equivalentes. O teste `isinstance(key, str)` logo no início evita uma recursão infinita: se a chave já é string e mesmo assim não foi encontrada, o método precisa desistir com `KeyError`, em vez de tentar converter para string de novo e cair no mesmo caminho indefinidamente. Implementação completa em [`_04_missing_and_defaultdict.py`](../code/chapter_03/_04_missing_and_defaultdict.py).

O comportamento de `__missing__` não é uniforme entre as classes base da biblioteca padrão:

| Classe base | `__missing__` é acionado em |
|---|---|
| `dict` puro (só implementando `__missing__`) | apenas `d[k]` |
| `UserDict` (só implementando `__missing__`) | `d[k]` e também `d.get(k)` |
| `abc.Mapping` mínima | depende de como `__getitem__` foi implementado |

---

## 3.5 Variações de Dict na Biblioteca Padrão

### 3.5.1 `OrderedDict`

Como o `dict` comum já preserva ordem de inserção desde o Python 3.7, `OrderedDict` deixou de ser necessário só para esse fim. Ainda vale a pena em três situações: quando a comparação `==` precisa levar a ordem em conta (o que `dict` comum não faz), quando se usa `move_to_end()`, útil na implementação de um cache LRU, e para manter compatibilidade com código escrito para versões anteriores do Python.

### 3.5.2 `ChainMap`

Mantém uma lista de mapeamentos consultados como se fossem um só, buscando na ordem em que foram passados ao construtor e parando na primeira ocorrência encontrada.

```python
d1 = dict(a=1, b=3)
d2 = dict(a=2, b=4, c=6)
chain = ChainMap(d1, d2)

chain['a']   # 1, encontrado em d1
chain['c']   # 6, não estava em d1, buscou em d2
```

> Escritas por meio do `ChainMap` afetam apenas o primeiro mapeamento da cadeia. É uma estrutura útil para implementar escopos aninhados, como no exemplo clássico `ChainMap(locals(), globals(), vars(builtins))`, que reproduz a ordem de busca de variáveis do próprio Python.

### 3.5.3 `Counter`

Mapeamento especializado em contagem de ocorrências, com suporte aos operadores `+` e `-` e ao método `most_common(n)`.

```python
ct = collections.Counter('abracadabra')
ct.update('aaaaazzz')
ct.most_common(3)   # [('a', 10), ('z', 3), ('b', 2)]
```

### 3.5.4 `shelve.Shelf`

Fornece armazenamento persistente de chaves string para objetos Python serializados via `pickle`. É subclasse de `abc.MutableMapping` e funciona como gerenciador de contexto, o que garante que o arquivo seja fechado corretamente ao sair do bloco `with`.

> O livro recomenda cautela com `pickle` de forma geral, citando o artigo "Pickle's nine flaws", de Ned Batchelder, para quem quiser entender melhor os riscos.

### 3.5.5 Por que estender `UserDict` em vez de `dict`

Herdar diretamente de `dict` para criar um tipo de mapeamento customizado parece o caminho natural, mas costuma trazer problemas: o tipo embutido usa atalhos internos escritos em C que às vezes ignoram métodos sobrescritos. `UserDict` evita isso porque não é subclasse de `dict`: encapsula um dict interno (o atributo `.data`) por composição, e delega as operações para ele.

```python
class StrKeyDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item
```

Como `UserDict` estende `MutableMapping`, métodos como `update()` e `get()` já vêm prontos, delegando corretamente para `__setitem__` e `__getitem__`. Isso torna essa versão de `StrKeyDict` mais curta que a anterior e, ao mesmo tempo, mais correta: toda chave inserida é convertida para string, inclusive durante a inicialização ou um `update`. Comparação lado a lado com `StrKeyDict0` em [`_04_missing_and_defaultdict.py`](../code/chapter_03/_04_missing_and_defaultdict.py); `ChainMap` e `Counter` em [`_05_dict_variants.py`](../code/chapter_03/_05_dict_variants.py).

---

## 3.6 Mapeamentos Imutáveis

A biblioteca padrão não tem um tipo de dict imutável, mas `types.MappingProxyType` cobre boa parte dos casos de uso: cria uma visão somente leitura e dinâmica sobre um mapeamento existente.

```python
from types import MappingProxyType

d = {1: 'A'}
d_proxy = MappingProxyType(d)

d_proxy[1]        # 'A'
d_proxy[2] = 'x'  # TypeError

d[2] = 'B'
d_proxy           # mappingproxy({1: 'A', 2: 'B'}), reflete a mudança feita em d
```

> O caso de uso citado no livro é expor uma coleção interna (por exemplo, portas de hardware em uma biblioteca de GPIO) sem correr o risco de o cliente da API modificar o mapeamento por engano. O proxy é dinâmico: mudanças no dicionário original continuam visíveis através dele, apenas não podem ser feitas diretamente por ele. Demonstração em [`_06_immutable_mappings.py`](../code/chapter_03/_06_immutable_mappings.py).

---

## 3.7 Views de Dicionário

`.keys()`, `.values()` e `.items()` devolvem views, não cópias. No Python 2, esses métodos criavam listas duplicando os dados existentes; no Python 3, as views são projeções somente leitura sobre a estrutura interna do dict, o que evita esse gasto extra de memória.

```python
d = dict(a=10, b=20, c=30)
values = d.values()

d['z'] = 99
values   # dict_values([10, 20, 30, 99]), já reflete a mudança
```

> Uma view acompanha o dicionário original em tempo real, sem precisar ser recriada a cada consulta. Views não são indexáveis (`values[0]` gera `TypeError`), e as classes `dict_keys`, `dict_values` e `dict_items` não podem ser instanciadas diretamente pelo código do usuário. Demonstração em [`_07_dict_views.py`](../code/chapter_03/_07_dict_views.py).

---

## 3.8 Consequências Práticas da Implementação por Tabela de Hash

Vários comportamentos de `dict` fazem mais sentido quando se lembra que a estrutura interna é uma tabela de hash:

- A busca por chave é próxima de O(1), independentemente do tamanho do dicionário, já que a posição é calculada diretamente a partir do hash da chave.
- Chaves precisam ser hashable, pelo motivo discutido em 3.3.1.
- A ordem de inserção é preservada desde o Python 3.7, como consequência de um layout de memória mais compacto adotado a partir do CPython 3.6.
- O custo em memória é maior do que um array simples de ponteiros, já que a tabela precisa manter em torno de um terço das posições vazias para continuar eficiente conforme cresce.
- A otimização de key-sharing dictionary (PEP 412, desde o Python 3.3) permite que instâncias de uma mesma classe compartilhem a tabela de hash usada por `__dict__`, reduzindo o uso de memória em torno de 10 a 20% em código orientado a objetos. Essa otimização só se mantém se todos os atributos forem definidos já dentro de `__init__`; criar atributos novos depois disso força Python a criar uma tabela separada só para aquela instância.

---

## 3.9 Conjuntos

Um `set` é uma coleção de elementos únicos e hashable. `frozenset` é a variante imutável e, justamente por isso, ela mesma é hashable, podendo ser elemento de outro `set`, algo que um `set` comum não pode fazer.

### 3.9.1 Para que servem, na prática

O uso mais óbvio é remover duplicatas:

```python
l = ['spam', 'spam', 'eggs', 'spam', 'bacon', 'eggs']
set(l)   # {'eggs', 'spam', 'bacon'}, ordem não preservada
```

Quando a ordem de primeira ocorrência importa, uma alternativa é usar `dict.fromkeys`, que preserva ordem como qualquer dict:

```python
list(dict.fromkeys(l).keys())   # ['spam', 'eggs', 'bacon']
```

Outro uso frequente é teste de pertencimento. Se o código faz `item in colecao` repetidamente e a coleção é grande, trocar de `list` para `set` costuma trazer ganho real de desempenho, pela mesma razão de tabela de hash discutida em 3.8.

O terceiro uso, talvez o mais interessante, é evitar laços explícitos ao comparar coleções. Contar quantos itens de uma coleção pequena (as "agulhas") aparecem em uma grande (o "palheiro"):

```python
found = len(needles & haystack)
```

faz o mesmo trabalho que:

```python
found = 0
for n in needles:
    if n in haystack:
        found += 1
```

com a vantagem de ser mais direto de ler, e um pouco mais rápido, desde que `needles` e `haystack` já sejam conjuntos (ou sejam convertidos: `set(needles) & set(haystack)`). Demonstração em [`_08_sets.py`](../code/chapter_03/_08_sets.py).

### 3.9.2 Sintaxe de literais

```python
s = {1, 2, 3}
vazio = set()
```

> `{}` cria um dict vazio, não um set vazio: é uma peculiaridade histórica da sintaxe, já que `{}` foi reservado para dict antes de `set` virar tipo embutido.

Compreensões de conjunto seguem a mesma lógica de listcomps e dictcomps:

```python
{n**2 for n in range(6)}
```

### 3.9.3 Operações de conjunto

| Operação | Operador | Método |
|---|---|---|
| Interseção | `s & z` | `s.intersection(z)` |
| União | `s \| z` | `s.union(z)` |
| Diferença | `s - z` | `s.difference(z)` |
| Diferença simétrica | `s ^ z` | `s.symmetric_difference(z)` |
| Subconjunto | `s <= z` | `s.issubset(z)` |
| Superconjunto | `s >= z` | `s.issuperset(z)` |
| Conjuntos disjuntos | | `s.isdisjoint(z)` |

As versões com atribuição aumentada (`&=`, `|=`, `-=`, `^=`) modificam o conjunto no lugar, e por isso não existem em `frozenset`, que é imutável por definição.

Métodos exclusivos de `set` mutável: `add(e)`, `remove(e)`, `discard(e)`, `pop()`, `clear()`.

---

## 3.10 Operações de Conjunto em Views de Dict

`dict_keys` e `dict_items` implementam boa parte da API de `frozenset`, o que permite tratar chaves ou itens de dicionários diretamente como conjuntos, sem precisar converter explicitamente.

```python
d1 = dict(a=1, b=2, c=3, d=4)
d2 = dict(b=20, d=40, e=50)

d1.keys() & d2.keys()   # {'b', 'd'}
```

Isso funciona também combinando com um `set` comum:

```python
s = {'a', 'e', 'i'}
d1.keys() & s   # {'a'}
```

> `dict_keys` sempre pode ser tratado como conjunto, já que chaves são hashable por definição. `dict_items` só se comporta como conjunto se todos os valores do dicionário também forem hashable; caso contrário a operação gera `TypeError: unhashable type`. Demonstração em [`_09_dict_views_as_sets.py`](../code/chapter_03/_09_dict_views_as_sets.py).

Esse recurso é útil, por exemplo, para comparar dois dicionários de configuração e descobrir rapidamente quais chaves foram adicionadas ou removidas entre duas versões, sem escrever um laço de comparação manual.

---

## Síntese do Capítulo

A sintaxe de dicts evoluiu bastante nas últimas versões de Python: compreensões, desempacotamento com `**`, os operadores `|`/`|=` e pattern matching estruturado. A biblioteca padrão complementa o `dict` básico com `defaultdict`, `ChainMap`, `Counter` e `OrderedDict`, cada um pensado para um problema específico. Para mapeamentos customizados, `UserDict` é a base recomendada, evitando as armadilhas de herdar diretamente de `dict`.

`setdefault` e `update` merecem atenção especial: o primeiro evita buscas redundantes ao lidar com valores mutáveis dentro de um dict, o segundo permite inicializar ou atualizar mapeamentos a partir de qualquer fonte compatível, seja outro mapeamento, um iterável de pares ou argumentos nomeados. `__missing__` é o mecanismo geral por trás do tratamento de chaves ausentes, usado internamente por `defaultdict` e também disponível para customização direta em subclasses.

Views de dicionário evitam cópias desnecessárias e, no caso de `dict_keys` e `dict_items`, suportam operações de conjunto. `set` e `frozenset` implementam a álgebra de conjuntos como operadores infixos, o que costuma tornar código de filtragem e comparação mais curto e mais claro do que a versão equivalente escrita com laços e condicionais.

No fundo, todos esses recursos convergem para a mesma estrutura de dados: a tabela de hash (3.8) é o que torna `dict` e `set` rápidos, exige chaves/elementos hashable e explica por que a ordem de inserção passou a ser preservada só a partir de uma reorganização interna, não por acaso de design.
