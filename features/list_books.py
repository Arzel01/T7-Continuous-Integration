"""
Loans management module for the CaféLibro Library Loan Manager.

This module handles the logic related to book loans, including retrieving 
active loans, checking due dates, and tracking borrowed books by members.
"""
import json

def get_member_loans(member_id, data_path='data.json'):
    """
    Return a list with the details of the books that a member has loaned.
    """
    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    member_loans = [loan for loan in data.get('loans', []) if loan['member_id'] == member_id]

    if not member_loans:
        return []

    loaned_books_details = []
    for loan in member_loans:
        for book in data.get('books', []):
            if book['isbn'] == loan['book_isbn']:
                loaned_books_details.append({
                    "isbn": book['isbn'],
                    "title": book['title'],
                    "author": book['author'],
                    "loan_date": loan['loan_date'],
                    "due_date": loan['due_date']
                })
                break

    return loaned_books_details
