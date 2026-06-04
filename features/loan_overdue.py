"""Módulo para generar reportes de préstamos vencidos en CaféLibro."""

import json
import sys
from datetime import datetime, date
import argparse


def load_database(filepath):
    """Carga la base de datos JSON desde la ruta provista."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find database file at '{filepath}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: The database file is not valid JSON.")
        sys.exit(1)


def report_overdue_loans(filepath, reference_date=None):
    """Busca en la base de datos los préstamos vencidos y genera un reporte."""
    data = load_database(filepath)

    books_lookup = {
        book['isbn']: book['title'] for book in data.get('books', [])
    }
    members_lookup = {
        member['id']: member['name'] for member in data.get('members', [])
    }

    if reference_date is None:
        current_date = date.today()
    else:
        try:
            current_date = datetime.strptime(reference_date, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format.")
            sys.exit(1)

    overdue_loans = []

    for loan in data.get('loans', []):
        due_date = datetime.strptime(loan['due_date'], "%Y-%m-%d").date()

        if due_date < current_date:
            overdue_loans.append({
                'book_title': books_lookup.get(
                    loan['book_isbn'], 'Unknown Book'
                ),
                'member_name': members_lookup.get(
                    loan['member_id'], 'Unknown Member'
                ),
                'due_date': loan['due_date'],
                'days_overdue': (current_date - due_date).days
            })

    print_report(overdue_loans, current_date)


def print_report(overdue_loans, current_date):
    """Imprime el reporte formateado en la consola."""
    date_str = current_date.strftime('%Y-%m-%d')
    print(f"\n--- CAFÉLIBRO OVERDUE REPORT (As of {date_str}) ---")

    if not overdue_loans:
        print("No overdue loans! All books are currently accounted for.")
        print("---------------------------------------------------------")
        return

    for idx, ol in enumerate(overdue_loans, 1):
        print(f"{idx}. {ol['book_title']}")
        print(f"   Checked out to: {ol['member_name']}")
        print(
            f"   Due Date:       {ol['due_date']} "
            f"({ol['days_overdue']} days overdue)"
        )
    print("---------------------------------------------------------\n")


if __name__ == "__main__":
    MSG = "CaféLibro Library Loan Manager"
    parser = argparse.ArgumentParser(description=MSG)
    parser.add_argument(
        "db_file", help="Path to the library database JSON file"
    )
    parser.add_argument(
        "--date",
        help="Optional: Simulate a specific current date (YYYY-MM-DD)",
        default=None
    )

    args = parser.parse_args()
    report_overdue_loans(args.db_file, args.date)
