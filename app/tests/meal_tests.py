import pytest
import requests as req
from unittest.mock import patch, MagicMock

from app.router import crud
from app.db.model import User


class TestGetMealFromApi:

    def test_returns_meal_data_on_success(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meals": [{"strMeal": "Carbonara", "idMeal": "52772"}]
        }

        with patch("app.router.crud.requests.get", return_value=mock_response):
            result = crud.get_meal_from_api("Carbonara")

        assert result is not None
        assert result["data"]["strMeal"] == "Carbonara"
        assert "52772" in result["url"]

    def test_returns_none_when_no_meals(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"meals": None}

        with patch("app.router.crud.requests.get", return_value=mock_response):
            result = crud.get_meal_from_api("unknowndish")

        assert result is None

    def test_returns_none_on_request_exception(self):
        with patch("app.router.crud.requests.get", side_effect=req.RequestException):
            result = crud.get_meal_from_api("anything")

        assert result is None


class TestAllMeals:

    def test_returns_empty_list(self, patch_get_db):
        result = crud.all_meals()
        assert result == []

    def test_returns_all_meals(self, sample_meal, patch_get_db):
        result = crud.all_meals()
        assert len(result) == 1
        assert result[0].title == "Spaghetti Carbonara"


class TestGetMealById:

    def test_returns_meal_by_id(self, sample_meal, patch_get_db):
        result = crud.get_meal_by_id(sample_meal.id)
        assert result is not None
        assert result.id == sample_meal.id

    def test_returns_none_for_invalid_id(self, patch_get_db):
        result = crud.get_meal_by_id("00000000-0000-0000-0000-000000000000")
        assert result is None


class TestGetMealFromDb:

    def test_returns_meal_by_title(self, sample_meal, patch_get_db):
        result = crud.get_meal_from_db("Spaghetti Carbonara")
        assert result is not None
        assert result.title == "Spaghetti Carbonara"

    def test_returns_none_if_not_found(self, patch_get_db):
        result = crud.get_meal_from_db("Nonexistent Dish")
        assert result is None


class TestGetMealsByUser:

    def test_returns_meals_for_user(self, sample_meal, sample_user, patch_get_db):
        result = crud.get_meals_by_user(sample_user.user_id)
        assert len(result) == 1
        assert result[0].user_id == sample_user.user_id

    def test_returns_empty_for_unknown_user(self, patch_get_db):
        result = crud.get_meals_by_user("00000000-0000-0000-0000-000000000000")
        assert result == []

    def test_does_not_return_other_users_meals(self, db_session, sample_meal, patch_get_db):
        other_user = User(username="other", password="x", birthdate=None)
        db_session.add(other_user)
        db_session.commit()

        result = crud.get_meals_by_user(other_user.user_id)
        assert result == []


class TestCreateMeal:

    def test_creates_meal_successfully(self, mock_ingredients_form, sample_user, patch_get_db, app):
        mock_api_result = {
            "data": {"strMeal": "Chicken Lemon", "idMeal": "12345"},
            "url": "https://www.themealdb.com/meal/12345",
        }

        with app.test_request_context():
            from flask import session
            session["user_id"] = sample_user.user_id

            with patch("app.router.crud.generate_meal_details", return_value="Chicken Lemon"):
                with patch("app.router.crud.get_meal_from_api", return_value=mock_api_result):
                    result = crud.create_meal(mock_ingredients_form)

        assert result.title == "Chicken Lemon"
        assert result.user_id == sample_user.user_id

    def test_raises_value_error_when_api_returns_none(self, mock_ingredients_form, patch_get_db, app):
        with app.test_request_context():
            with patch("app.router.crud.generate_meal_details", return_value="Unknown"):
                with patch("app.router.crud.get_meal_from_api", return_value=None):
                    with pytest.raises(ValueError):
                        crud.create_meal(mock_ingredients_form)