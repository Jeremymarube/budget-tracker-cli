import sys
import os
from datetime import datetime
import bcrypt


# Am Adding project root so "lib" is recognized
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.models import session
from lib.models.expense import Expense
from lib.models.category import Category
from lib.models.user import User

def register():
    username = input("Choose a username: ").strip()
    
    # Check if username already exists
    if session.query(User).filter_by(username=username).first():
        print("Username already exists!")
        return None

    # Ask for password twice
    while True:
        password = input("Choose a password: ").strip()
        confirm_password = input("Confirm password: ").strip()
        
        if password != confirm_password:
            print("Passwords do not match. Try again.")
        elif len(password) < 4: 
            print("Password too short. Must be at least 4 characters.")
        else:
            break

    
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create user
    user = User(username=username, password=hashed_pw)
    
    try:
        session.add(user)
        session.commit()
        print(f"User {username} registered successfully!")
        return user
    except Exception as e:
        session.rollback()
        print(f"Error creating user: {e}")
        return None


def login():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    # filtering by username
    user = session.query(User).filter_by(username=username).first()
    
    # Checking password against hashed value
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        print(f"\nHello {username}, welcome!\n")
        return user
    else:
        print("Invalid credentials!")
        return None


def add_transaction(user):
    categories = session.query(Category).all()
    if not categories:
        print("No categories found. Add a category first.")
        return

    print("\nChoose category:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.name}")

    try:
        category_choice = int(input("Enter category number: "))
        if category_choice < 1 or category_choice > len(categories):
            raise ValueError
    except ValueError:
        print("Invalid category choice.")
        return

    chosen_category = categories[category_choice - 1]

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    type_ = input("Type (income/expense): ").strip().lower()
    if type_ not in ["income", "expense"]:
        print("Invalid type. Must be 'income' or 'expense'.")
        return

    date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if date_input:
        try:
            trans_date = datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Using today.")
            trans_date = datetime.now()
    else:
        trans_date = datetime.now()

    new_transaction = Expense(
        amount=amount,
        transaction_type=type_,
        category_id=chosen_category.id,
        user_id=user.id,
        date=trans_date
    )

    session.add(new_transaction)
    session.commit()
    print(f"{type_.capitalize()} transaction added successfully!")


def view_balance(user):
    income_total = sum(exp.amount for exp in user.expenses if exp.transaction_type == "income")
    expense_total = sum(exp.amount for exp in user.expenses if exp.transaction_type == "expense")
    balance = income_total - expense_total
    print(f"\nYour current balance: ${balance:.2f}")
    print(f"   Total Income: ${income_total:.2f}, Total Expenses: ${expense_total:.2f}")

def spending_report(user):
    expenses = [exp for exp in user.expenses if exp.transaction_type == "expense"]
    if not expenses:
        print("No expense transactions found.")
        return

    filter_choice = input("Filter by date? (y/n): ").strip().lower()
    if filter_choice == "y":
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        end_date = input("End date (YYYY-MM-DD): ").strip()
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            expenses = [e for e in expenses if start <= e.date <= end]
        except ValueError:
            print("Invalid date format. Showing all transactions.")

    if not expenses:
        print("No expenses in this range.")
        return

    report = {}
    for exp in expenses:
        cat_name = exp.category.name if exp.category else "Uncategorized"
        report[cat_name] = report.get(cat_name, 0) + exp.amount

    print("\nSpending by Category:")
    for cat, total in sorted(report.items(), key=lambda x: x[1], reverse=True):
        print(f"- {cat}: ${total:.2f}")

def manage_categories():
    while True:
        print("\nCategory Management:")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Delete Category")
        print("4. Back to Main Menu")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Enter new category name: ").strip()
            if session.query(Category).filter_by(name=name).first():
                print("Category already exists!")
            else:
                session.add(Category(name=name))
                session.commit()
                print(f"Category '{name}' added successfully!")
        elif choice == "2":
            categories = session.query(Category).all()
            if not categories:
                print("No categories found.")
            else:
                print("Categories:")
                for c in categories:
                    print(f"- {c.name}")
        elif choice == "3":
            categories = session.query(Category).all()
            if not categories:
                print("No categories to delete.")
                continue
            for i, c in enumerate(categories, 1):
                print(f"{i}. {c.name}")
            try:
                num = int(input("Enter category number to delete: "))
                category = categories[num - 1]
                if category.expenses:
                    print("Cannot delete category with transactions!")
                else:
                    session.delete(category)
                    session.commit()
                    print(f"Category '{category.name}' deleted.")
            except (ValueError, IndexError):
                print("Invalid choice.")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def edit_delete_transactions(user):
    expenses = user.expenses
    if not expenses:
        print("No transactions found.")
        return

    print("\nYour Transactions:")
    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp.category.name if exp.category else 'Uncategorized'} | ${exp.amount:.2f} | {exp.transaction_type} | {exp.date.strftime('%Y-%m-%d')}")

    try:
        num = int(input("Enter transaction number to edit/delete: "))
        expense = expenses[num - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    print("1. Edit Transaction")
    print("2. Delete Transaction")
    action = input("Choose: ").strip()

    if action == "1":
        try:
            new_amount = float(input("Enter new amount: "))
            expense.amount = new_amount
            session.commit()
            print("Transaction updated!")
        except ValueError:
            print("Invalid amount.")
    elif action == "2":
        session.delete(expense)
        session.commit()
        print("Transaction deleted!")
    else:
        print("Invalid choice.")

def main_menu(user):
    while True:
        print("1. Add Transaction")
        print("2. View Balance")
        print("3. Spending Report")
        print("4. Manage Categories")
        print("5. Edit/Delete Transactions")
        print("6. Logout")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_transaction(user)
        elif choice == "2":
            view_balance(user)
        elif choice == "3":
            spending_report(user)
        elif choice == "4":
            manage_categories()
        elif choice == "5":
            edit_delete_transactions(user)
        elif choice == "6":
            print(f"\nGoodbye {user.username}, see you next time!\n")
            break
        else:
            print("Invalid choice. Try again.")

def main():
    while True:
        print("\nWelcome to Budget Tracker!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            user = register()
            if user:
                main_menu(user)
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        elif choice == "3":
            print("Goodbye! Thank you for using Budget Tracker.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
