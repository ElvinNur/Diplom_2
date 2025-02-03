import requests
import pytest
import allure
from config import LOGIN_URL
from data import EXISTING_USER

class TestAuthLogin:

    @allure.title("Успешная авторизация пользователя")
    @allure.description("Тест проверяет успешную авторизацию пользователя с валидными данными.")
    def test_login_with_valid_credentials(self):
        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(LOGIN_URL, json=EXISTING_USER)
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_body = response.json()
            assert response_body["success"] is True, "Response 'success' is not True"


    @allure.title("Неуспешная авторизация пользователя с некорректными данными")
    @allure.description("Тест проверяет, что авторизация пользователя с некорректными данными возвращает ошибку.")
    @pytest.mark.parametrize("user_data", [
        {"email": "eldiabl@yandex.ru", "password": "password123"}, 
        {"email": "eldiablo@yandex.ru", "password": "password12"},
        {"email": "eldiabl@yandex.ru", "password": "password12"},
    ])
    def test_login_with_invalid_credentials(self, user_data):
        with allure.step("Отправка запроса на авторизацию с некорректными данными"):
            response = requests.post(LOGIN_URL, json=user_data)
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 401, f"Unexpected status code: {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_body = response.json()
            assert response_body["success"] is False, "Response 'success' should be False"
            assert response_body["message"] == "email or password are incorrect", (
                f"Unexpected message: {response_body['message']}"
            )
