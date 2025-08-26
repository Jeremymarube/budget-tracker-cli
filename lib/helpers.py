from .models import session, Category, Expense

def add_expense():
    categories = session.query(Category).all()
    if not categories:
        print("No categories found. Please seed the database first.")
        return
    
    print("Choose a category:")
    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat.name}")
    
    choice = int(input("Enter choice: ")) - 1
    if choice < 0 or choice >= len(categories):
        print("Invalid category!")
        return
    
    amount = float(input("Enter amount: "))
    type_ = input("Type (income/expense): ").lower()

    if type_ not in ["income", "expense"]:
        print("Invalid type!")
        return

    expense = Expense(amount=amount, type=type_, category=categories[choice])
    session.add(expense)
    session.commit()
    print("Expense added successfully!")

def view_balance():
    income = sum(e.amount for e in session.query(Expense).filter_by(type="income").all())
    expense = sum(e.amount for e in session.query(Expense).filter_by(type="expense").all())
    balance = income - expense
    print(f"Your current balance is: ${balance}")

def spending_report():
    expenses = session.query(Expense).filter_by(type="expense").all()
    report = {}
    for e in expenses:
        report[e.category.name] = report.get(e.category.name, 0) + e.amount

    print("Spending by category:")
    for cat, total in report.items():
        print(f"{cat}: ${total}")