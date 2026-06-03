"""
Módulo de gestión de préstamos de la biblioteca CaféLibro.
Proporciona funciones para cargar, guardar y registrar préstamos
de libros controlando las reglas de negocio establecidas.
"""

import json
import os
from datetime import datetime, timedelta

DB_FILE = "data.json"


def load_data():
    """Carga el estado actual del JSON."""
    if not os.path.exists(DB_FILE):
        return {"members": [], "books": [], "loans": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    """Guarda el estado en el JSON con formato legible."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def loan_book(book_isbn, member_id):
    """
    Registra el préstamo de un libro a un miembro.
    Aplica las reglas de negocio de la biblioteca.
    """
    data = load_data()

    # 1. Validar si el libro existe en el catálogo
    book_exists = any(b["isbn"] == book_isbn for b in data["books"])
    if not book_exists:
        raise ValueError(
            f"Error: El libro con ISBN {book_isbn} no existe en el catálogo."
        )

    # 2. Validar si el miembro está registrado
    member_exists = any(m["id"] == member_id for m in data["members"])
    if not member_exists:
        raise ValueError(
            f"Error: El miembro con ID {member_id} no está registrado."
        )

    # 3. Validar si el libro YA está prestado
    is_already_loaned = any(l["book_isbn"] == book_isbn for l in data["loans"])
    if is_already_loaned:
        raise ValueError(
            f"Error: El libro {book_isbn} ya se encuentra prestado."
        )

    # 4. Validar si el miembro ya alcanzó el límite de 3 libros
    current_loans_count = sum(
        1 for l in data["loans"] if l["member_id"] == member_id
    )
    if current_loans_count >= 3:
        raise ValueError(
            f"Error: El miembro {member_id} ya tiene el límite máximo "
            "de 3 libros prestados."
        )

    # Si pasa todas las validaciones, se calcula la fecha de vencimiento
    today = datetime.now().date()
    due_date = today + timedelta(days=14)

    new_loan = {
        "book_isbn": book_isbn,
        "member_id": member_id,
        "loan_date": str(today),
        "due_date": str(due_date),
    }

    data["loans"].append(new_loan)
    save_data(data)
    return (
        f"Éxito: Libro {book_isbn} prestado a {member_id} "
        f"hasta el {due_date}."
    )