"""
Módulo de gestión de préstamos de la biblioteca CaféLibro.
Proporciona funciones para cargar, guardar y registrar préstamos
de libros controlando las reglas de negocio establecidas.
"""
import json
import os
import argparse

DATA_FILE = 'library_data.json'



def load_data():
    """Load data from the JSON file or return a default empty structure."""
    if not os.path.exists(DATA_FILE):
        return {"books": [], "members": [], "loans": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    """Save the provided data dictionary to the JSON file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def register_member(member_id, name):
    """Register a new member with a unique ID and name."""
    data = load_data()

    if "members" not in data:
        data["members"] = []

    for member in data["members"]:
        if member["id"] == member_id:
            raise ValueError(
                f"Member with ID '{member_id}' is already registered."
            )

    data["members"].append({"id": member_id, "name": name})
    save_data(data)

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CaféLibro CLI")
    parser.add_argument(
        "--register", nargs=2, metavar=('ID', 'NAME'), help="Register member"
    )
    args = parser.parse_args()

    if args.register:
        try:
            register_member(args.register[0], args.register[1])
            print(
                f"Member '{args.register[1]}' (ID: {args.register[0]}) "
                "registered successfully."
            )
        except ValueError as e:
            print(f"Error: {e}")
