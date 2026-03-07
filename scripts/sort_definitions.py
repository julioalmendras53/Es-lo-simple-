import re
import json

def sort_definitions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar el inicio y fin del objeto diccionario
    # Usamos una expresión regular para capturar todo el objeto diccionario
    # Buscamos desde 'const diccionario = {' hasta el '};' que cierra el objeto.
    # Nota: El objeto puede contener llaves anidadas, por lo que necesitamos un contador de llaves.
    
    start_match = re.search(r'const diccionario = \{', content)
    if not start_match:
        print("No se encontró 'const diccionario = {'")
        return

    start_idx = start_match.end() - 1
    
    # Encontrar la llave de cierre correspondiente
    brace_count = 0
    end_idx = -1
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    
    if end_idx == -1:
        print("No se encontró la llave de cierre del diccionario")
        return

    diccionario_str = content[start_idx:end_idx]
    
    # Extraer las entradas del diccionario. 
    # Las entradas suelen tener el formato: "clave": { ... } o clave: { ... }
    # Vamos a usar una técnica más robusta: buscar las claves de primer nivel.
    
    # Eliminamos el primer '{' y el último '}'
    inner_content = diccionario_str[1:-1].strip()
    
    # Dividir por entradas. Las entradas están separadas por comas en el nivel superior.
    entries = []
    current_entry = ""
    nested_braces = 0
    in_quotes = False
    quote_char = ""
    
    for char in inner_content:
        if char in ('"', "'") and (not current_entry or current_entry[-1] != '\\'):
            if not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char:
                in_quotes = False
        
        if not in_quotes:
            if char == '{':
                nested_braces += 1
            elif char == '}':
                nested_braces -= 1
            
            if char == ',' and nested_braces == 0:
                entries.append(current_entry.strip())
                current_entry = ""
                continue
        
        current_entry += char
    
    if current_entry.strip():
        entries.append(current_entry.strip())

    # Función para obtener la clave de una entrada
    def get_key(entry):
        # Buscar la clave antes del primer ':'
        match = re.match(r'^\s*["\']?([^"\':]+)["\']?\s*:', entry)
        if match:
            return match.group(1).lower()
        return entry.lower()

    # Ordenar las entradas alfabéticamente por clave
    # Usamos locale-aware sorting o simplemente minúsculas para consistencia básica
    entries.sort(key=get_key)

    # Reconstruir el string del diccionario
    new_diccionario_str = "{\n    " + ",\n    ".join(entries) + "\n  }"
    
    # Reemplazar en el contenido original
    new_content = content[:start_idx] + new_diccionario_str + content[end_idx:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Diccionario ordenado exitosamente en {file_path}")

if __name__ == "__main__":
    sort_definitions('/home/ubuntu/Es-lo-simple-/libro.html')
