import json
import argparse
from datetime import datetime, date


def load_database(filepath):
    """Loads the JSON database from the provided filepath."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find database file at '{filepath}'")
        exit(1)
    except json.JSONDecodeError:
        print("Error: The database file is not valid JSON.")
        exit(1)


def report_overdue_loans(filepath, reference_date=None):
    """Checks the database for loans past their due date and prints a report."""
    data = load_database(filepath)
    
    # Create lookup dictionaries for faster and more readable cross-referencing
    books_lookup = {book['isbn']: book['title'] for book in data.get('books', [])}
    members_lookup = {member['id']: member['name'] for member in data.get('members', [])}
    
    # Default to today's date if no reference date is provided
    if reference_date is None:
        current_date = date.today()
    else:
        try:
            current_date = datetime.strptime(reference_date, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format.")
            exit(1)

    overdue_loans = []
    
    for loan in data.get('loans', []):
        due_date = datetime.strptime(loan['due_date'], "%Y-%m-%d").date()
        
        # A loan is overdue if the due date is strictly before the current date
        if due_date < current_date:
            overdue_loans.append({
                'book_title': books_lookup.get(loan['book_isbn'], 'Unknown Book'),
                'member_name': members_lookup.get(loan['member_id'], 'Unknown Member'),
                'due_date': loan['due_date'],
                'days_overdue': (current_date - due_date).days
            })
            
    # Output the report
    print(f"\n--- CAFÉLIBRO OVERDUE REPORT (As of {current_date.strftime('%Y-%m-%d')}) ---")
    
    if not overdue_loans:
        print("No overdue loans! All books are currently accounted for.")
        print("---------------------------------------------------------")
        return

    for idx, ol in enumerate(overdue_loans, 1):
        print(f"{idx}. {ol['book_title']}")
        print(f"   Checked out to: {ol['member_name']}")
        print(f"   Due Date:       {ol['due_date']} ({ol['days_overdue']} days overdue)")
    print("---------------------------------------------------------\n")


if __name__ == "__main__":
    # Setup argparse so staff can run this easily from the terminal
    parser = argparse.ArgumentParser(description="CaféLibro Library Loan Manager")
    parser.add_argument("db_file", help="Path to the library database JSON file")
    parser.add_argument("--date", help="Optional: Simulate a specific current date (YYYY-MM-DD)", default=None)
    
    args = parser.parse_args()
    report_overdue_loans(args.db_file, args.date)