import requests
import pytest
import allure
from config import BASE_URL
from data import EXISTING_USER
from helpers import generate_unique_user

class TestUserCreationAPI:

    @allure.title("Создание уникального пользователя")
    @allure.description("Тест проверяет успешное создание уникального пользователя и удаление его после теста.")
    def test_create_unique_user(self, delete_user):
        unique_user = generate_unique_user()
        
        with allure.step("Отправка запроса на создание пользователя"):
            response = requests.post(BASE_URL, json=unique_user)
        
        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
            response_body = response.json()
            assert response_body["success"] is True, "Response 'success' is not True"

        # Передаем access_token в фикстуру для удаления пользователя
        delete_user(response_body["accessToken"])

    @allure.title("Создание уже существующего пользователя")
    @allure.description("Тест проверяет, что нельзя создать пользователя с уже существующими данными.")
    def test_create_existing_user(self):
        with allure.step("Попытка создания уже существующего пользователя"):
            requests.post(BASE_URL, json=EXISTING_USER)

            response = requests.post(BASE_URL, json=EXISTING_USER)
        
        with allure.step("Проверка ошибки создания"):
            assert response.status_code == 403, f"Unexpected status code: {response.status_code}"
            response_body = response.json()
            assert response_body["success"] is False, "Response 'success' is not False"
            assert response_body["message"] == "User already exists", "Error message mismatch"

    @allure.title("Создание пользователя с отсутствующим обязательным полем")
    @allure.description("Тест проверяет, что нельзя создать пользователя, если отсутствует обязательное поле.")
    @pytest.mark.parametrize("missing_field, user_data", [
        ("email", {"password": "securepassword", "name": "NoEmailUser"}),
        ("password", {"email": "nopassword@example.com", "name": "NoPasswordUser"}),
        ("name", {"email": "noname@example.com", "password": "securepassword"}),
    ])
    def test_create_user_missing_field(self, missing_field, user_data):
        with allure.step(f"Попытка создания пользователя без поля '{missing_field}'"):
            response = requests.post(BASE_URL, json=user_data)
        
        with allure.step("Проверка ошибки создания"):
            assert response.status_code == 403, f"Unexpected status code: {response.status_code}"
            response_body = response.json()
            assert response_body["success"] is False, "Response 'success' is not False"
            assert response_body["message"] == "Email, password and name are required fields", "Error message mismatch"
