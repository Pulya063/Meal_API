from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Date, Column, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.db.database import Base

class Meal(Base):
    __tablename__ = "meal"
    id = Column(String ,primary_key=True, default=lambda: str(uuid4()))
    title = Column(String)
    description = Column(String)
    date = Column(Date, default=date.today())
    user_id = Column(String, ForeignKey('user.user_id'))

    user = relationship("User", back_populates="meals")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }

class User(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    username = Column(String)
    password = Column(String)
    date = Column(Date)


    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.user_id,
            "username": self.username,
            "password": self.password,
            "meals": self.meals
        }