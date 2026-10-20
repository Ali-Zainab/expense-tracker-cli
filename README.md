# Expense Tracker CLI (Python)

A command-line tool to track your spending. Expenses are saved to a local
`expenses.json` file, so your data stays between runs.

## Features
- Add, list, and delete expenses
- Total spending, or total for one category
- Summary of spending per category
- Input validation (amounts must be positive)
- Unit tests with `pytest`

## Requirements
Python 3.8+ (no extra libraries needed to run it). `pytest` is only needed for tests.

## Usage
```
python expense_tracker.py add 250 food --note "lunch"
python expense_tracker.py add 40 travel
python expense_tracker.py list
python expense_tracker.py total
python expense_tracker.py total --category food
python expense_tracker.py summary
python expense_tracker.py delete 1
```

## Run the tests
```
pip install pytest
pytest
```

## Project structure
```
expense-tracker-cli/
├── expense_tracker.py       # the app
├── test_expense_tracker.py  # unit tests
├── README.md
└── .gitignore
```

## Concepts used
Functions, `argparse` subcommands, JSON file storage, input validation, unit testing.
