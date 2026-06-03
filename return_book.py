"""
Library Loan Management Module.

This module handles library transactions, specifically processing book returns 
and updating the local JSON database file.

Dependencies:
    - json (standard library)

Data Files:
    - data.json: Expects a JSON file with a structure containing a "loans" key:
        {
            "loans": [
                {"member_id": "M101", "book_isbn": "B999"},
                ...
            ]
        }
"""
import json

def return_book(member_id, book_id):
    """
    Process the return of a borrowed book by removing its loan record.

    This function reads the loan database from 'data.json', searches for a match
    matching the provided member ID and book ISBN, removes the record if found,
    and updates the file.

    Parameters
    ----------
    member_id : str or int
        The unique identifier of the library member returning the book.
    book_id : str or int
        The ISBN or unique identifier of the book being returned.

    Returns
    -------
    dict
        The full, updated loan database dictionary if the return is successful.
        If no matching loan record is found, returns a dictionary containing
        an error message: {"Error": "Loan does not exist"}.
    """
    with open("data.json", "r", encoding="utf-8") as file:
        loaded_data = json.load(file)
        for loan in loaded_data["loans"]:
            if loan["book_isbn"] == book_id and loan["member_id"] == member_id:
                loaded_data["loans"].remove(loan)
                with open("data.json", "w", encoding="utf-8") as file:
                    json.dump(loaded_data, file, indent=4, encoding="utf-8")
                return loaded_data
    loaded_data = {"Error": "Loan does not exist"}
    return loaded_data
