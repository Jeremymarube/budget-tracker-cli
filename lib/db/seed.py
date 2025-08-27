import sys
import os
import bcrypt

# Adding project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from lib.models import Base, engine, session
from lib.models.category import Category
from lib.models.expense import Expense
from lib.models.user import User

# Reset database (drop and recreate tables)
print("Resetting database...")
Base.metadata.drop_all(engine)   # drop existing tables
Base.metadata.create_all(engine) # create tables fresh

# ---- Seed Categories ----
categories = [
    Category(name="Food"),
    Category(name="Transport"),
    Category(name="Entertainment")
]
session.add_all(categories)
session.commit()

# ---- Seed User ----
hashed_pw = bcrypt.hashpw("1234".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
user = User(username="Jeremy", password=hashed_pw)
session.add(user)
session.commit()

print("Database seeded successfully!")
