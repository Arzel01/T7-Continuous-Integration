"""Unit tests for the library management module."""
import os
import json
import pytest
from library import register_member, DATA_FILE


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Fixture to clean up the data file before and after each test."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

    yield

    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


def test_register_new_member():
    """Test the successful registration of a new member."""
    result = register_member("123", "John Doe")
    assert result is True

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data["members"]) == 1
    assert data["members"][0]["id"] == "123"
    assert data["members"][0]["name"] == "John Doe"


def test_register_duplicate_member():
    """Test that registering a member with an existing ID raises an error."""
    register_member("123", "John Doe")

    with pytest.raises(ValueError) as excinfo:
        register_member("123", "Jane Smith")

    assert "is already registered" in str(excinfo.value)