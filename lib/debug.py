from .models import session, Category, Expense

print("Categories:", session.query(Category).all())
print("Expenses:", session.query(Expense).all())
