import pytest
import allure
import requests
from config import LOGIN_URL, DELETE_URL
from data import EXISTING_USER

@pytest.fixture
def headers():
    """Получение заголовков авторизации."""
    with allure.step("Авторизация пользователя и получение токена"):
        login_response = requests.post(LOGIN_URL, json=EXISTING_USER)
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"
        access_token = login_response.json()["accessToken"]
        return {"Authorization": access_token}


@pytest.fixture
def delete_user():
    """Фикстура для удаления пользователя после теста"""
    access_token = None  # Переменная для хранения токена

    def _set_token(token):
        nonlocal access_token
        access_token = token

    yield _set_token  # Передаем функцию установки токена в тест

    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(DELETE_URL, headers=headers)