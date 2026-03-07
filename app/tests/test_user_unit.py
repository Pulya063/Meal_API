import unittest
from unittest.mock import MagicMock
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.db.model import User
from app.router import crud
from app.other.oauth import hash_password
from werkzeug.exceptions import Unauthorized, NotFound

class TestUser(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_user_model(self):
        user = User(
            username="test_user",
            password="hashed_password",
            birthdate=date(2000, 1, 1)
        )
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.password, "hashed_password")
        self.assertEqual(user.birthdate, date(2000, 1, 1))

    def test_create_user(self):
        form = MagicMock()
        form.login.data = "new_user"
        form.password.data = "password123"
        form.birthdate.data = date(1995, 5, 20)

        user = crud.create_user(self.session, form)

        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.username, "new_user")
        
        saved_user = crud.get_user_by_username(self.session, "new_user")
        self.assertIsNotNone(saved_user)

    def test_login_success(self):
        password = "securepassword"
        user = User(
            username="login_user", 
            password=hash_password(password), 
            birthdate=date(1990, 1, 1)
        )
        self.session.add(user)
        self.session.commit()

        form = MagicMock()
        form.username.data = "login_user"
        form.password.data = password

        token_data = crud.login_user(self.session, form)
        
        self.assertIn("access_token", token_data)
        self.assertEqual(token_data["token_type"], "bearer")

    def test_login_wrong_password(self):
        user = User(
            username="wrong_pass_user", 
            password=hash_password("correct"), 
            birthdate=date(1990, 1, 1)
        )
        self.session.add(user)
        self.session.commit()

        form = MagicMock()
        form.username.data = "wrong_pass_user"
        form.password.data = "wrong"

        with self.assertRaises(Unauthorized):
            crud.login_user(self.session, form)

    def test_login_not_found(self):
        form = MagicMock()
        form.username.data = "ghost_user"
        form.password.data = "any"

        with self.assertRaises(NotFound):
            crud.login_user(self.session, form)
