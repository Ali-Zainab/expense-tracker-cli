import pytest

from expense_tracker import (
    add_expense,
    delete_expense,
    load_expenses,
    save_expenses,
    summary_by_category,
    total,
)


def test_add_expense_assigns_incrementing_ids():
    expenses = []
    first = add_expense(expenses, 50, "Food")
    second = add_expense(expenses, 20, "Travel")
    assert first["id"] == 1
    assert second["id"] == 2
    assert first["category"] == "food"


def test_add_expense_rejects_non_positive_amount():
    with pytest.raises(ValueError):
        add_expense([], 0, "food")
    with pytest.raises(ValueError):
        add_expense([], -5, "food")


def test_delete_expense():
    expenses = []
    add_expense(expenses, 10, "food")
    assert delete_expense(expenses, 1) is True
    assert delete_expense(expenses, 99) is False
    assert expenses == []


def test_total_and_category_total():
    expenses = []
    add_expense(expenses, 100, "food")
    add_expense(expenses, 50.5, "travel")
    add_expense(expenses, 25, "food")
    assert total(expenses) == 175.5
    assert total(expenses, "Food") == 125


def test_summary_by_category():
    expenses = []
    add_expense(expenses, 100, "food")
    add_expense(expenses, 50, "travel")
    add_expense(expenses, 25, "food")
    assert summary_by_category(expenses) == {"food": 125, "travel": 50}


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "data.json"
    expenses = []
    add_expense(expenses, 30, "snacks", note="chips")
    save_expenses(expenses, path)
    assert load_expenses(path) == expenses


def test_load_missing_file_returns_empty(tmp_path):
    assert load_expenses(tmp_path / "nope.json") == []
