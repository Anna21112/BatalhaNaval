#Conversão de letras para índices e vice-versa

def letra_para_indice(letra):
    """Converte 'A' -> 0, 'B' -> 1, ..."""
    return ord(letra.upper()) - ord('A')

def indice_para_letra(indice):
    """Converte 0 -> 'A', 1 -> 'B', ..."""
    return chr(ord('A') + indice)