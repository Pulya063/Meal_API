import pytest
from unittest.mock import MagicMock
from werkzeug.exceptions import NotFound, Unauthorized, Conflict

from app.router import crud
from app.db.model import User


class TestGetUserByUsername:

    def test_returns_user_if_exists(self, sample_user, patch_get_db):
        result = crud.get_user_by_username("testuser")
        assert result is not None
        assert result.username == "testuser"

    def test_returns_none_if_not_exists(self, patch_get_db):
        result = crud.get_user_by_username("ghost")
        assert result is None


class TestGetUserById:

    def test_returns_user_by_id(self, sample_user, patch_get_db):
        result = crud.get_user_by_id(sample_user.user_id)
        assert result is not None
        assert result.user_id == sample_user.user_id

    def test_returns_none_for_invalid_id(self, patch_get_db):
        result = crud.get_user_by_id("00000000-0000-0000-0000-000000000000")
        assert result is None


class TestAllUsers:

    def test_returns_empty_list(self, patch_get_db):
        result = crud.all_users()
        assert result == []

    def test_returns_all_users(self, sample_user, patch_get_db):
        result = crud.all_users()
        assert len(result) == 1
        assert result[0].username == "testuser"

    def test_returns_multiple_users(self, db_session, patch_get_db):
        for i in range(3):
            db_session.add(User(username=f"user{i}", password="x", birthdate=None))
        db_session.commit()

        result = crud.all_users()
        assert len(result) == 3


class TestCreateUser:

    def test_creates_user_successfully(self, mock_register_form, patch_get_db):
        result = crud.create_user(mock_register_form)
        assert result is not None
        assert result.username == "newuser"

    def test_password_is_hashed(self, mock_register_form, patch_get_db):
        result = crud.create_user(mock_register_form)
        assert result.password != "password123"
        assert result.password.startswith("$pbkdf2")

    def test_raises_conflict_on_duplicate_username(self, sample_user, patch_get_db):
        form = MagicMock()
        form.username.data = sample_user.username
        form.password.data = "anything"
        form.birthdate.data = sample_user.birthdate

        with pytest.raises(Conflict):
            crud.create_user(form)

    def test_saves_correct_birthdate(self, mock_register_form, patch_get_db):
        from datetime import date
        result = crud.create_user(mock_register_form)
        assert result.birthdate == date(1999, 5, 20)


class TestLoginUser:

    def test_login_success(self, mock_login_form, patch_get_db, app):
        with app.test_request_context():
            result = crud.login_user(mock_login_form)
            assert "access_token" in result
            assert result["token_type"] == "bearer"

    def test_sets_session_on_login(self, mock_login_form, sample_user, patch_get_db, app):
        with app.test_request_context():
            from flask import session
            crud.login_user(mock_login_form)
            assert session.get("user_id") == sample_user.user_id

    def test_raises_not_found_for_unknown_user(self, patch_get_db, app):
        form = MagicMock()
        form.username.data = "nobody"
        form.password.data = "whatever"

        with app.test_request_context():
            with pytest.raises(NotFound):
                crud.login_user(form)

    def test_raises_unauthorized_for_wrong_password(self, sample_user, patch_get_db, app):
        form = MagicMock()
        form.username.data = sample_user.username
        form.password.data = "wrongpassword"

        with app.test_request_context():
            with pytest.raises(Unauthorized):
                crud.login_user(form)