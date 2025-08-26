import sys
import os
import bcrypt

# Adding project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from lib.models import Base, engine, session
from lib.models.category import Category
from lib.models.expense import Expense
from lib.models.user import User

# reset database (drop and recreate tables)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# sample categories
food = Category(name="Food")
transport = Category(name="Transport")
entertainment = Category(name="Entertainment")

session.add_all([food, transport, entertainment])
session.commit()

# sample user with hashed password
hashed_pw = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
user = User(username="Jeremy", password=hashed_pw)
session.add(user)
session.commit()

print("Database seeded")
