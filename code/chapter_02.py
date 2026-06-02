import array
import sys
import os


symbols = "café©"


# 2.2a: for loop tradicional
codes = []
for s in symbols:
    codes.append(ord(s))
print(codes)

# 2.2b: listcomp equivalente
codes = [ord(s) for s in symbols]
print(codes)


# 2.2c: map + filter
beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
print(beyond_ascii)

# 2.2d: listcomp com filtro (equivalente, mais legivel)
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
print(beyond_ascii)

# 2.2e: walrus operator evita calcular ord(s) duas vezes
beyond_ascii = [code for s in symbols if (code := ord(s)) > 127]
print(beyond_ascii)


# 2.2f: produto cartesiano com listcomp
cores = ["preto", "branco"]
tamanhos = ["P", "M", "G"]

camisetas = [(cor, tam) for cor in cores for tam in tamanhos]
print(camisetas)


# 2.2g: genexp, nenhuma lista intermediaria e criada
codigos = array.array("I", (ord(s) for s in symbols))
print(codigos)

# 2.2h: produto cartesiano com genexp
for camiseta in (f"{cor} {tam}" for cor in cores for tam in tamanhos):
    print(camiseta)


# ---------------------------------------------------------------------------
# 2.4 Tuplas
# ---------------------------------------------------------------------------

# 2.4a: tupla como registro — posição tem significado
brasilia = (-15.7797, -47.9297)
lat, lon = brasilia
print(f"Brasília — lat: {lat}, lon: {lon}")

registro_csv = ("São Paulo", 2024, 11_451_245)
cidade, ano, pop = registro_csv
print(f"{cidade} tinha {pop:,} hab. em {ano}")


# 2.4b: desempacotamento posicional
# swap sem variável temporária
a, b = 10, 20
a, b = b, a
print(f"a={a}, b={b}")

# ignorar campos com _ (variável descartável)
_, ano, _ = registro_csv
print(f"Ano extraído: {ano}")

# capturar o restante com * (retorna lista, mesmo vindo de tupla)
primeiro, *meio, ultimo = (1, 2, 3, 4, 5)
print(f"primeiro={primeiro}, meio={meio}, ultimo={ultimo}")


# 2.4c: comparação de memória tuple vs list
t = (1, 2, 3, 4, 5)
l = [1, 2, 3, 4, 5]
print(f"tuple: {sys.getsizeof(t)} bytes")
print(f"list:  {sys.getsizeof(l)} bytes")


# 2.4d: tupla com item mutável — imutabilidade é da referência, não do conteúdo
t_mut = ([1, 2], [3, 4])
t_mut[0].append(99)   # OK: muta a lista interna
print(f"t_mut após append: {t_mut}")

try:
    t_mut[0] = [9, 9]  # erro: não pode trocar a referência
except TypeError as e:
    print(f"TypeError: {e}")

# tupla com mutável não é hashable (não pode ser chave de dict)
try:
    hash(t_mut)
except TypeError as e:
    print(f"Não é hashable: {e}")


# ---------------------------------------------------------------------------
# 2.5 Descompactando Coleções
# ---------------------------------------------------------------------------

# 2.5a: path split — ignorar diretório, pegar só o nome do arquivo
_, filename = os.path.split("/home/user/docs/report.pdf")
print(f"filename: {filename}")

# pegar apenas o último segmento de um caminho
*_, last = "/usr/local/bin/python".split("/")
print(f"last: {last}")


# 2.5b: * recolhe o excesso e sempre retorna lista
primeiro, *resto = range(5)
print(f"primeiro={primeiro}, resto={resto}")

*inicio, ultimo = range(5)
print(f"inicio={inicio}, ultimo={ultimo}")

primeiro, *meio, ultimo = range(6)
print(f"primeiro={primeiro}, meio={meio}, ultimo={ultimo}")

a, b, *_ = (10, 20, 30, 40, 50)  # descarta o restante
print(f"a={a}, b={b}")


# 2.5c: * em chamadas de função e literais (PEP 448)
def soma(x, y, z):
    return x + y + z

args = (1, 2, 3)
print(soma(*args))

l1 = [1, 2, 3]
l2 = [4, 5]
merged = [*l1, *l2, 6]
print(f"merged: {merged}")

d1 = {"a": 1}
d2 = {"b": 2}
merged_dict = {**d1, **d2, "c": 3}
print(f"merged_dict: {merged_dict}")


# 2.5d: desempacotamento aninhado — query SQL com LIMIT 1
query_result = [("Tokyo", "JP", 37_400_000)]
[(city, _, pop)] = query_result
print(f"{city}: {pop:,}")

# coordenadas aninhadas em tupla
metro_areas = [
    ("Tokyo",     "JP", 36.933, (35.689722,  139.691667)),
    ("São Paulo", "BR", 19.649, (-23.547778, -46.635833)),
]

for name, _, _, (lat, lon) in metro_areas:
    if lon <= 0:
        print(f"{name}: {lat:.4f}N, {lon:.4f}W")
