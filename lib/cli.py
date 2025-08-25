import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from models import session
from models.expense import Expense
from models.category import Category
from models.user import User


def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if session.query(User).filter_by(username=username).first():
        print("Username already exists.")
        return
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    print(f"✅ User {username} registered!")

def login():
    username = input("Username: ")
    password = input("Password: ")
    user = session.query(User).filter_by(username=username, password=password).first()
    if not user:
        print("Invalid username or password.")
        return
    print(f"\nHello, {user.username}!\n")
    user_menu(user)

def user_menu(user):
    while True:
        print("1. Add Transaction")
        print("2. View Balance")
        print("3. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            add_transaction(user)
        elif choice == "2":
            view_balance(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice")

def add_transaction(user):
    try:
        amount = int(input("Amount: "))
    except ValueError:
        print("Invalid amount. Enter a number without $ sign.")
        return

    # Show existing categories
    print("Available categories:")
    categories = session.query(Category).all()
    for cat in categories:
        print(f"- {cat.name}")
    
    category_name = input("Category: ")
    category = session.query(Category).filter_by(name=category_name).first()
    if not category:
        print("Category not found")
        return

    type_ = input("Type (income/expense): ").lower()
    if type_ not in ["income", "expense"]:
        print("Invalid type")
        return

    expense = Expense(
        amount=amount,
        transaction_type=type_,  # column name in Expense
        category=category,
        user=user
    )
    session.add(expense)
    session.commit()
    print("✅ Transaction added!")

def view_balance(user):
    income = session.query(Expense).filter_by(user=user, transaction_type="income").all()
    expense = session.query(Expense).filter_by(user=user, transaction_type="expense").all()
    balance = sum(i.amount for i in income) - sum(e.amount for e in expense)
    print(f"Your current balance is: ${balance}")

def main():
    while True:
        print("Welcome to Budget Tracker!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
