# 💰 Personal Budget and Expense Tracker
 - A **command-line interface (CLI)** personal budget and expense tracker built in Python using **SQLAlchemy ORM**. This tool allows users to manage their income, expenses, and categories efficiently, with detailed reporting.

---

## Example Workflow (Demo)
 ```
 Welcome to Budget Tracker!
  1. Register
  2. Login
  3. Exit
 Enter choice: 1

 Choose a username: john_doe
 Choose a password: [hidden]
 Confirm password: [hidden]
 User john_doe registered successfully!
```

---

## ✨ Features
  -  **Secure User Authentication** - Registration and login with bcrypt password hashing
  -  **Transaction Management** - Add, edit, and delete income/expense transactions
  -  **Balance Tracking** - View current balance with income/expense breakdown
  -  **Spending Reports** - Detailed reports with optional date filtering
  -  **Category Management** - Create, view, and delete expense categories
  -  **Date Support** - Custom transaction dates or automatic timestamping
  -  **Error Handling** - Robust error handling with transaction rollbacks

---

## Installation
1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd budget-tracker-cli
   ```
2. Install dependencies using Pipenv:
   ```
   pipenv install
   pipenv shell
   ```
 ---

## 🛠️ Setup
1. Seed the database with initial categories and a default user:
   ```
   python lib/db/seed.py
   ```
2. Apply Alembic migrations (if applicable):
   ```
   alembic upgrade head
   ```
## 🚀 Usage
Run the main program:
```
python lib/cli.py
```
## 🎯 Main menu options
 1. Register – Create a new user account.

 2. Login – Log in to your existing account.

 3. Add Transaction – Add income or expense with category, amount, date, and type.

 4. View Balance – Displays total income, expenses, and net balance.

 5. Spending Report – Shows spending by category, optionally filtered by date range.

 6. Manage Categories – Add, view, or delete categories.

 7. Edit/Delete Transactions – Modify or remove any existing transactions.

 8. Logout / Exit – End session and exit CLI.

 ---

 ## 🗂️ Project structure
 ```
 BUDGET-TRACKER-CLI/
├── .venv/                # Virtual environment
├── lib/
│   ├── db/
│   │   ├── __pycache__/
│   │   └── seed.py       # Database seeding script
│   └── models/
│       ├── __pycache__/
│       ├── __init__.py   # Database configuration
│       ├── category.py   # Category model
│       ├── expense.py    # Expense model
│       └── user.py       # User model
├── cli.py                # Main CLI application
├── debug.py              # Debug utilities
├── helpers.py            # Helper functions
├── migrations/           # Alembic migration files
├── .gitignore           # Git ignore file
├── alembic.ini          # Alembic configuration
├── budget.db            # SQLite database file
├── Pipfile              # Dependencies and virtual environment
├── Pipfile.lock         # Locked dependency versions
└── README.md            # This file
```

---

## 📦 Dependencies
 - SQLAlchemy - ORM for database interactions
 - bcrypt - Secure password hashing
 - Pipenv - Virtual environment management

---

## ✍️ Author
   **Jeremy Marube**

---   



   
 
