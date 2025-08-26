from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.models import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # one user has many expenses
    expenses = relationship("Expense", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username})>"