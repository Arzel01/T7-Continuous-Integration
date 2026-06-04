"""
Unit tests for the loans management module.

This test suite verifies the behavior of the get_member_loans function,
ensuring correct tracking of active loans, empty results for members without 
loans, and proper handling of missing database files using pytest fixtures.
"""
import json
import pytest
from features.list_books import get_member_loans

@pytest.fixture(name="mocked_data_file")
def fixture_mocked_data_file(tmp_path):
    """Creates a temporal data.json with controlled test data."""
    test_data = {
        "books": [
            { "isbn": "978-0132350884",
            "title": "Clean Code", 
            "author": "Robert C. Martin" },
            { "isbn": "978-1491950296",
            "title": "Building Microservices", 
            "author": "Sam Newman" }
        ],
        "loans": [
            { "book_isbn": "978-0132350884", "member_id": "M001",
            "loan_date": "2026-05-10", "due_date": "2026-05-24" },
            { "book_isbn": "978-1491950296", "member_id": "M001",
            "loan_date": "2026-05-20", "due_date": "2026-06-03" }
        ]
    }
    file_path = tmp_path / "mock_data.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)
    return file_path

def test_get_member_loans_with_active_loans(mocked_data_file):
    """Tests if a member with active loans returns the correct list."""
    loans = get_member_loans("M001", data_path=mocked_data_file)
    assert len(loans) == 2
    assert loans[0]["title"] == "Clean Code"
    assert loans[1]["title"] == "Building Microservices"
    assert loans[0]["due_date"] == "2026-05-24"

def test_get_member_loans_no_loans(mocked_data_file):
    """Tests if either a non-existant member or a member without loans returns an empty list."""
    loans = get_member_loans("M004", data_path=mocked_data_file)
    assert len(loans) == 0
    assert isinstance(loans, list)

def test_get_member_loans_file_not_found():
    """Tests the behavior when the JSON file does not exist."""
    loans = get_member_loans("M001", data_path="non_existant_path.json")
    assert len(loans) == 0
