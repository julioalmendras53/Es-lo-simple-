
import re
import random
from collections import defaultdict

# Leer el libro HTML
with open("../libro.html", "r", encoding="utf-8") as f:
    html = f.read()

# Quitar etiquetas HTML
texto = re.sub(r"<[^>]+>", " ", html)
texto = re.sub(r"\s+", " ", texto).strip()

# Separar palabras
palabras = texto.split()

# Crear modelo semilla tipo Markov
modelo = defaultdict(list)

for i in range(len(palabras) - 2):
    clave = (palabras[i], palabras[i+1])
    siguiente = palabras[i+2]
    modelo[clave].append(siguiente)

def generar(inicio=None, longitud=80):
    if inicio:
        partes = inicio.split()
        if len(partes) >= 2:
            clave = (partes[-2], partes[-1])
        else:
            clave = random.choice(list(modelo.keys()))
    else:
        clave = random.choice(list(modelo.keys()))

    salida = [clave[0], clave[1]]

    for _ in range(longitud):
        opciones = modelo.get(clave)
        if not opciones:
            clave = random.choice(list(modelo.keys()))
            salida.extend([clave[0], clave[1]])
            continue

        nueva = random.choice(opciones)
        salida.append(nueva)
        clave = (clave[1], nueva)

    return " ".join(salida)

if __name__ == "__main__":
    print("=== LLM SEMILLA DEL LIBRO DEL INFINITO ===")
    print()
    print(generar(longitud=120))
