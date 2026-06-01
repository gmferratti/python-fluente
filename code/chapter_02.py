import array


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
