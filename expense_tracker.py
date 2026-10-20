"""Expense Tracker CLI: track spending from the terminal, saved to a JSON file."""

import argparse
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses(path=DATA_FILE):
    """Read expenses from the JSON file. Returns [] if missing or unreadable."""
    path = Path(path)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_expenses(expenses, path=DATA_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses, amount, category, note="", when=None):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    next_id = max((e["id"] for e in expenses), default=0) + 1
    expense = {
        "id": next_id,
        "amount": round(amount, 2),
        "category": category.strip().lower(),
        "note": note,
        "date": when or date.today().isoformat(),
    }
    expenses.append(expense)
    return expense


def delete_expense(expenses, expense_id):
    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            return True
    return False


def total(expenses, category=None):
    if category:
        category = category.strip().lower()
        return round(sum(e["amount"] for e in expenses if e["category"] == category), 2)
    return round(sum(e["amount"] for e in expenses), 2)


def summary_by_category(expenses):
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    return {cat: round(amt, 2) for cat, amt in sorted(totals.items())}


def print_table(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    print(f"{'ID':<4} {'Date':<11} {'Category':<12} {'Amount':>9}  Note")
    print("-" * 50)
    for e in expenses:
        print(f"{e['id']:<4} {e['date']:<11} {e['category']:<12} {e['amount']:>9.2f}  {e['note']}")


def build_parser():
    parser = argparse.ArgumentParser(description="Simple expense tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add an expense")
    p_add.add_argument("amount", type=float)
    p_add.add_argument("category")
    p_add.add_argument("--note", default="")

    sub.add_parser("list", help="List all expenses")

    p_total = sub.add_parser("total", help="Show total spending")
    p_total.add_argument("--category", default=None)

    sub.add_parser("summary", help="Spending per category")

    p_del = sub.add_parser("delete", help="Delete an expense by ID")
    p_del.add_argument("id", type=int)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    expenses = load_expenses()

    if args.command == "add":
        try:
            e = add_expense(expenses, args.amount, args.category, args.note)
        except ValueError as err:
            print(f"Error: {err}")
            return 1
        save_expenses(expenses)
        print(f"Added #{e['id']}: {e['amount']:.2f} on {e['category']}")
    elif args.command == "list":
        print_table(expenses)
    elif args.command == "total":
        label = f" ({args.category})" if args.category else ""
        print(f"Total{label}: {total(expenses, args.category):.2f}")
    elif args.command == "summary":
        for cat, amt in summary_by_category(expenses).items():
            print(f"{cat:<12} {amt:>9.2f}")
    elif args.command == "delete":
        if delete_expense(expenses, args.id):
            save_expenses(expenses)
            print(f"Deleted #{args.id}")
        else:
            print(f"No expense with ID {args.id}")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
