"""Módulo para registrar nuevos libros en el catálogo de CaféLibro."""

import json


def load_database(filepath):
    """Carga la base de datos JSON desde la ruta provista."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"members": [], "books": [], "loans": []}
    except json.JSONDecodeError as exc:
        raise ValueError(
            "El archivo de base de datos no contiene un JSON válido."
        ) from exc


def save_database(filepath, data):
    """Guarda los datos actualizados en el archivo JSON."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def register_book(filepath, isbn, title, author="Desconocido"):
    """Registra un libro en el catálogo validando que el ISBN sea único."""
    try:
        data = load_database(filepath)
    except ValueError as e:
        return False, str(e)

    if 'books' not in data:
        data['books'] = []

    for book in data['books']:
        if book['isbn'] == isbn:
            return (
                False,
                f"Error: Ya existe un libro con el código '{isbn}' "
                f"('{book['title']}')."
            )

    new_book = {
        "isbn": isbn,
        "title": title,
        "author": author
    }

    data['books'].append(new_book)
    save_database(filepath, data)

    return (
        True,
        f"Libro '{title}' registrado exitosamente con el código {isbn}."
    )


if __name__ == "__main__":
    DB_PRUEBA = "library.json"

    print("--- EJECUTANDO PRUEBA INDIVIDUAL DE REGISTRO DE LIBROS ---")

    ISBN_TEST = "978-0131103627"
    TITLE_TEST = "The C Programming Language"
    AUTHOR_TEST = "Brian W. Kernighan"

    exito, mensaje = register_book(
        DB_PRUEBA, ISBN_TEST, TITLE_TEST, AUTHOR_TEST
    )
    print(f"\nIntento 1:\nResultado: {exito}\nMensaje: {mensaje}")

    exito_dup, mensaje_dup = register_book(
        DB_PRUEBA, ISBN_TEST, TITLE_TEST, AUTHOR_TEST
    )
    print(f"\nIntento 2 (Duplicado):\nResultado: {exito_dup}\nMensaje: {mensaje_dup}")

    print("\n-------------------------------------------------------------")