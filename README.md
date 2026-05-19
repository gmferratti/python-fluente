# Python Fluente: Clube do Livro · LHC

Acompanhamento da leitura coletiva do livro **Python Fluente** de Luciano Ramalho, realizada pelo clube do livro do [Laboratório Hacker de Campinas (LHC)](https://lhc.net.br).

Livro online (2ª edição): <https://pythonfluente.com/2/>

---

## Sobre o livro

**Python Fluente** é considerado a referência definitiva para quem quer deixar de *usar* Python e passar a *pensar* em Python. Luciano Ramalho percorre o modelo de dados da linguagem de ponta a ponta (métodos especiais, protocolos, generadores, decoradores, concorrência) mostrando como as abstrações do Python foram projetadas e como tirar o máximo delas escrevendo código idiomático, legível e eficiente.

A 2ª edição (2022) incorpora as novidades do Python 3.10+: tipos estruturais, `match/case`, `TypeVar`, `ParamSpec` e muito mais.

---

## Estrutura do repositório

```
python-fluente/
├── code/          # scripts Python com os exemplos de cada capítulo
│   └── chapter_XX.py
└── notes/         # anotações conceituais e mapas mentais por capítulo
    └── chapter_XX.md
```

Cada capítulo gera dois artefatos:

| Artefato | O que contém |
|---|---|
| `code/chapter_XX.py` | Implementações executáveis dos exemplos discutidos no encontro |
| `notes/chapter_XX.md` | Conceitos-chave, mapas de métodos especiais, comparações e resumos práticos |

---

## Progresso

| # | Capítulo | Notas | Código |
|---|---|---|---|
| 01 | O Modelo de Dados do Python | [notes](notes/chapter_01.md) | [code](code/chapter_01.py) |
| 02 | Uma Coleção de Sequências | — | — |
| 03 | Dicionários e Conjuntos | — | — |
| 04 | Texto versus Bytes | — | — |
| 05 | Tipos de Dados com Anotações | — | — |
| 06 | Referências a Objetos, Mutabilidade e Reciclagem | — | — |
| 07 | Funções como Objetos de Primeira Classe | — | — |
| 08 | Dicas de Tipo em Funções | — | — |
| 09 | Decoradores e Closures | — | — |
| 10 | Design com Decoradores | — | — |
| 11 | Um Array Pythonico de Sequências | — | — |
| 12 | Protocolos e Tipagem Estrutural | — | — |
| 13 | Interfaces, Protocolos e ABCs | — | — |
| 14 | Herança: para o Bem ou para o Mal | — | — |
| 15 | Mais Tipos em Classes e Funções | — | — |
| 16 | Sobrecarga de Operadores | — | — |
| 17 | Iteradores, Geradores e Classes Clássicas | — | — |
| 18 | with, match e mais | — | — |
| 19 | Concorrência com Threads | — | — |
| 20 | Concurrent Futures | — | — |
| 21 | asyncio | — | — |
| 22 | asyncio além do básico | — | — |
| 23 | Atributos de Instância e de Classe | — | — |
| 24 | Atributos e Descritores | — | — |
| 25 | Metaprogramação com Classes | — | — |

## Como usar este repositório

1. Clone o repositório:
   ```bash
   git clone <url-do-repo>
   cd python-fluente
   ```

2. Execute os exemplos de um capítulo:
   ```bash
   python code/chapter_01.py
   ```

3. Leia as anotações conceituais em `notes/chapter_XX.md` antes ou depois do encontro para consolidar o que foi discutido.

---

## Sobre o LHC

O [Laboratório Hacker de Campinas](https://lhc.net.br) é um hackerspace localizado em Campinas/SP dedicado à cultura maker, hardware livre, software livre e aprendizado colaborativo. O clube do livro é uma das iniciativas regulares da comunidade.
