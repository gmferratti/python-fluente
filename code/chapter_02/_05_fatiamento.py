"""
Fatiamento (2.7).

`s[a:b:c]` é açúcar sintático para `s.__getitem__(slice(a, b, c))`. Nomear a
fatia com `slice(...)` evita números mágicos ao trabalhar com dados de
largura fixa, como um extrato de compras.
"""

INVOICE = """
0.....6.................40........52...55........
1909  Pimoroni PiBrella                       $17.50
1489  6mm Tactile Switch x20                   $4.95
1510  Panavise Jr. - PV-201                    $28.00
1601  PiTFT Mini Kit 320x240                   $34.95
"""

SKU = slice(0, 6)
DESCRIPTION = slice(6, 40)
UNIT_PRICE = slice(40, 52)


def fatias_nomeadas_invoice():
    """Nomear fatias com `slice(...)` deixa o código autoexplicativo."""
    linhas = INVOICE.split("\n")[2:]  # ignora a linha vazia inicial e a régua de cabeçalho
    resultado = []
    for linha in linhas:
        if linha:
            resultado.append((linha[DESCRIPTION].strip(), linha[UNIT_PRICE].strip()))
    return resultado


def atribuindo_a_uma_fatia():
    """Escrever numa fatia pode encolher ou crescer a sequência mutável."""
    l = list(range(10))
    l[2:5] = [20, 30]      # substitui 3 itens por 2 -> encolhe
    l[2:5] = [100]         # substitui 3 itens por 1 -> encolhe de novo
    del l[5:7]             # apaga um trecho
    return l
