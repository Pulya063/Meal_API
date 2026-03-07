from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Date, Column, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.db.database import Base

class Meal(Base):
    __tablename__ = "meal"
    id = Column(String ,primary_key=True, default=lambda: str(uuid4()))
    title = Column(String)
    url = Column(String)
    date = Column(Date, default=date.today())
    user_id = Column(String, ForeignKey('user.user_id'))

    user = relationship("User", back_populates="meals")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "calories": self.calories,
            "date": self.date.isoformat() if self.date else None
        }

class User(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    username = Column(String)
    password = Column(String)
    birthdate = Column(Date)


    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.user_id,
            "username": self.username,
            "password": self.password,
            "date": self.date.isoformat() if self.date else None,
            "meals": [meal.to_dict() for meal in self.meals]
        }