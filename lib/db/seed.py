import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from lib.models import Base, engine, session
from lib.models.category import Category
from lib.models.expense import Expense
from lib.models.user import User

# Reset database: am dropping and recreating tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Seed categories
categories = [
    Category(name="Food"),
    Category(name="Transport"),
    Category(name="Entertainment")
]
session.add_all(categories)

# Optional: seed a default user for demo
default_user = User(username="Jeremy", password="1234")
session.add(default_user)

session.commit()

print(" Database seeded!")
