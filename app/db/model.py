from datetime import date
from uuid import uuid4

from sqlalchemy import String, Date, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base

class Meal(Base):
    __tablename__ = "meal"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String)
    url = Column(String)
    date = Column(Date, default=date.today())
    user_id = Column(String, ForeignKey('user.user_id'))

    user = relationship("User", back_populates="meals")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
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
            "birthdate": self.birthdate.isoformat() if self.birthdate else None,
            "meals": [meal.to_dict() for meal in self.meals]
        }
