from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from lib.models import Base

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)  # "income" or "expense"
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("Category")
    user = relationship("User", back_populates="expenses")
