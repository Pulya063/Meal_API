import pytest
from datetime import date
from contextlib import contextmanager
from unittest.mock import MagicMock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.model import User, Meal
from app.other.oauth import hash_password
from app.main import app as flask_app


TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(setup_db):
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def patch_get_db(db_session, monkeypatch):
    @contextmanager
    def mock_get_db():
        try:
            yield db_session
            db_session.commit()
        except Exception:
            db_session.rollback()
            raise

    monkeypatch.setattr("app.router.crud.get_db", mock_get_db)


@pytest.fixture
def app(patch_get_db):
    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False
    flask_app.config["SECRET_KEY"] = "test-secret"
    with flask_app.app_context():
        yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_user(db_session) -> User:
    user = User(
        username="testuser",
        password=hash_password("password123"),
        birthdate=date(2000, 1, 15),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_meal(db_session, sample_user) -> Meal:
    meal = Meal(
        title="Spaghetti Carbonara",
        url="https://www.themealdb.com/meal/52772",
        user_id=sample_user.user_id,
    )
    db_session.add(meal)
    db_session.commit()
    db_session.refresh(meal)
    return meal


@pytest.fixture
def mock_register_form():
    form = MagicMock()
    form.username.data = "newuser"
    form.password.data = "password123"
    form.birthdate.data = date(1999, 5, 20)
    return form


@pytest.fixture
def mock_login_form(sample_user):
    form = MagicMock()
    form.username.data = sample_user.username
    form.password.data = "password123"
    return form


@pytest.fixture
def mock_ingredients_form():
    form = MagicMock()
    form.ingredients.data = "chicken, garlic, lemon"
    return form