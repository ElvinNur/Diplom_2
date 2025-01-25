import requests
import pytest
import allure

class TestAuthLogin:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api/auth/login"
    
    @pytest.fixture
    def existing_user(self):
        """Параметры для уже существующего пользователя."""
        return {
            "email": "eldiablo@yandex.ru",
            "password": "password123",
            "name": "Username"
        }

    @allure.title("Успешная авторизация пользователя")
    @allure.description("Тест проверяет успешную авторизацию пользователя с валидными данными.")
    def test_login_with_valid_credentials(self, existing_user):
        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(self.BASE_URL, json=existing_user)
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_body = response.json()
            assert "accessToken" in response_body, "Key 'accessToken' not found in response"
            assert response_body["accessToken"].startswith("Bearer "), "AccessToken format is incorrect"

            assert "refreshToken" in response_body, "Key 'refreshToken' not found in response"
            assert len(response_body["refreshToken"]) > 0, "RefreshToken is empty"

            assert response_body["success"] is True, "Response 'success' is not True"
            assert "user" in response_body, "Key 'user' not found in response"
            assert response_body["user"]["email"] == existing_user["email"], "Email mismatch"
            assert response_body["user"]["name"] == existing_user["name"], "Name mismatch"

    @allure.title("Неуспешная авторизация пользователя с некорректными данными")
    @allure.description("Тест проверяет, что авторизация пользователя с некорректными данными возвращает ошибку.")
    @pytest.mark.parametrize("user_data", [
        {"email": "eldiabl@yandex.ru", "password": "password123"}, 
        {"email": "eldiablo@yandex.ru", "password": "password12"},
        {"email": "eldiabl@yandex.ru", "password": "password12"},
    ])
    def test_login_with_invalid_credentials(self, user_data):
        with allure.step("Отправка запроса на авторизацию с некорректными данными"):
            response = requests.post(self.BASE_URL, json=user_data)
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 401, f"Unexpected status code: {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_body = response.json()
            assert response_body["success"] is False, "Response 'success' should be False"
            assert response_body["message"] == "email or password are incorrect", (
                f"Unexpected message: {response_body['message']}"
            )
