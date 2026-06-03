import json
import sys


def load_database(filepath):
    """Carga la base de datos JSON desde la ruta provista."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Si el archivo no existe, inicializa la estructura base
        return {"members": [], "books": [], "loans": []}
    except json.JSONDecodeError:
        raise ValueError("El archivo de base de datos no contiene un JSON válido.")


def save_database(filepath, data):
    """Guarda los datos actualizados en el archivo JSON."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def register_book(filepath, isbn, title, author="Desconocido"):
    """
    Registra un libro en el catálogo después de verificar que el código sea único.
    
    Retorna (True, "Mensaje de éxito") si se registró,
    o (False, "Mensaje de error") si rompe alguna regla.
    """
    try:
        data = load_database(filepath)
    except ValueError as e:
        return False, str(e)
    
    if 'books' not in data:
        data['books'] = []
        
    # Regla de negocio: El código (ISBN) debe ser único
    for book in data['books']:
        if book['isbn'] == isbn:
            return False, f"Error: Ya existe un libro con el código/ISBN '{isbn}' ('{book['title']}')."
            
    new_book = {
        "isbn": isbn,
        "title": title,
        "author": author
    }
    
    data['books'].append(new_book)
    save_database(filepath, data)
    
    return True, f"Libro '{title}' registrado exitosamente con el código {isbn}."


# --- BLOQUE DE PRUEBA INDIVIDUAL ---
if __name__ == "__main__":
    # Datos de prueba locales
    DB_PRUEBA = "data.json"
    
    print("--- EJECUTANDO PRUEBA INDIVIDUAL DE REGISTRO DE LIBROS ---")
    
    # Intento 1: Registrar un libro nuevo
    isbn_test = "922-4435103607"
    title_test = "Scrum Framework"
    author_test = "Carlos Mera"
    
    exito, mensaje = register_book(DB_PRUEBA, isbn_test, title_test, author_test)
    print(f"\nIntento 1 (Libro Nuevo):\nResultado: {'Éxito' if exito else 'Fallo'}\nMensaje: {mensaje}")
    
    # Intento 2: Intentar registrar el MISMO libro para probar la regla de unicidad
    exito_duplicado, mensaje_duplicado = register_book(DB_PRUEBA, isbn_test, title_test, author_test)
    print(f"\nIntento 2 (Probar Duplicado con mismo ISBN):\nResultado: {'Éxito' if exito_duplicado else 'Fallo'}\nMensaje: {mensaje_duplicado}")
    
    print("\n-------------------------------------------------------------")