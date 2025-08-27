from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
engine = create_engine("sqlite:///budget.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Import models so that they are registered with Base
from .category import Category
from .expense import Expense
from .user import User

# Create tables if they do not exist
Base.metadata.create_all(engine)
