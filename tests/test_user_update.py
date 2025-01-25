import requests
import pytest
import allure

class TestUserUpdate:
    BASE_URL = "https://stellarburgers.nomoreparties.site"
    LOGIN_URL = f"{BASE_URL}/api/auth/login"
    UPDATE_URL = f"{BASE_URL}/api/auth/user"

    @pytest.fixture
    def valid_user(self):
        """Данные существующего пользователя."""
        return {
            "email": "mistereldiablo@example.com",
            "password": "securepassword123",
            "name": "Username"
        }

    @pytest.fixture
    def updated_user_data(self):
        """Данные для обновления пользователя."""
        return {
            "name": "UpdatedName",
            "email": "missiseldiablo@example.com"
        }

    @allure.title("Обновление данных пользователя с авторизацией")
    @allure.description("Тест проверяет успешное обновление данных пользователя при наличии авторизации.")
    def test_update_user_with_auth(self, valid_user, updated_user_data):
        """Тест обновления данных пользователя с авторизацией."""
        with allure.step("Авторизация пользователя и получение токена"):
            login_response = requests.post(self.LOGIN_URL, json=valid_user)
            assert login_response.status_code == 200, f"Login failed: {login_response.text}"
            access_token = login_response.json()["accessToken"]

        with allure.step("Обновление данных пользователя"):
            headers = {"Authorization": access_token}
            update_response = requests.patch(self.UPDATE_URL, json=updated_user_data, headers=headers)

            assert update_response.status_code == 200, f"Update failed: {update_response.text}"
            response_body = update_response.json()
            assert response_body["success"] is True, "Expected 'success' to be True"
            assert response_body["user"]["name"] == updated_user_data["name"], "Name mismatch"
            assert response_body["user"]["email"] == updated_user_data["email"], "Email mismatch"

        with allure.step("Восстановление исходных данных пользователя"):
            restore_response = requests.patch(
                self.UPDATE_URL,
                json={"name": valid_user["name"], "email": valid_user["email"]},
                headers=headers
            )
            assert restore_response.status_code == 200, f"Restore failed: {restore_response.text}"
            restore_body = restore_response.json()

            assert restore_body["success"] is True, "Expected 'success' to be True during restore"
            assert restore_body["user"]["name"] == valid_user["name"], "Restored name mismatch"
            assert restore_body["user"]["email"] == valid_user["email"], "Restored email mismatch"

    @allure.title("Попытка обновления данных пользователя без авторизации")
    @allure.description("Тест проверяет, что сервер возвращает ошибку при попытке обновления данных пользователя без авторизации.")
    def test_update_user_without_auth(self, updated_user_data):
        """Тест обновления данных пользователя без авторизации."""
        with allure.step("Отправка запроса на обновление данных без токена"):
            update_response = requests.patch(self.UPDATE_URL, json=updated_user_data)

        with allure.step("Проверка ответа сервера"):
            assert update_response.status_code == 401, f"Unexpected status code: {update_response.status_code}"
            response_body = update_response.json()
            assert response_body["success"] is False, "Expected 'success' to be False"
            assert response_body["message"] == "You should be authorised", (
                f"Unexpected message: {response_body['message']}"
            )