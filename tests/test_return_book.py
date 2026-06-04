"""Module for testing the return_book functionality."""

from features.return_book import return_book

correct_dic = {
    "members": [
        { "id": "M001", "name": "Alex Otero" },
        { "id": "M002", "name": "Kelly Silva" },
        { "id": "M003", "name": "Ronald Criollo" },
        { "id": "M004", "name": "Maria Jose" }
    ],
    "books": [
        { "isbn": "978-0132350884", "title": "Clean Code",
        "author": "Robert C. Martin"},
        { "isbn": "978-0201616224", "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt"},
        { "isbn": "978-0134494166", "title": "Design Patterns", "author":
        "Erich Gamma"},
        { "isbn": "978-1491950296", "title": "Building Microservices",
        "author": "Sam Newman"},
        { "isbn": "978-0131103627", "title": "The C Programming Language",
        "author": "Brian W. Kernighan"},
        { "isbn": "978-0596007126", "title": "Head First Design Patterns",
        "author": "Eric Freeman"},
        { "isbn": "978-0132145374", "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell"}
    ],
    "loans": [
        {
        "book_isbn": "978-0201616224",
        "member_id": "M001",
        "loan_date": "2026-05-15",
        "due_date": "2026-05-29"
        },
        {
        "book_isbn": "978-0134494166",
        "member_id": "M001",
        "loan_date": "2026-06-01",
        "due_date": "2026-06-15"
        },
        {
        "book_isbn": "978-1491950296",
        "member_id": "M002",
        "loan_date": "2026-05-20",
        "due_date": "2026-06-03"
        },
        {
        "book_isbn": "978-0131103627",
        "member_id": "M003",
        "loan_date": "2026-06-02",
        "due_date": "2026-06-16"
        }
    ]
}

def test_loan_exists():
    """Test that a book is successfully returned if the loan exists."""
    assert return_book("M001", "978-0132350884") == correct_dic

def test_loan_not_exists():
    """Test that an error message is returned if the loan does not exist."""
    assert return_book("M003", "978-0201616224") == {"Error": "Loan does not exist"}
