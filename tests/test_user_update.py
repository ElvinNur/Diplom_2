import requests
import pytest
import allure
from config import LOGIN_URL, UPDATE_URL
from data import UPDATED_USER_DATA, NEW_USER

class TestUserUpdate:
    @allure.title("Обновление данных пользователя с авторизацией")
    @allure.description("Тест проверяет успешное обновление данных пользователя при наличии авторизации.")
    def test_update_user_with_auth(self):
        """Тест обновления данных пользователя с авторизацией."""
        with allure.step("Регистрация пользователя и получение токена"):
            login_response = requests.post(LOGIN_URL, json=NEW_USER)
            assert login_response.status_code == 200, f"Login failed: {login_response.text}"
            access_token = login_response.json()["accessToken"]

        with allure.step("Обновление данных пользователя"):
            headers = {"Authorization": access_token}
            update_response = requests.patch(UPDATE_URL, json=UPDATED_USER_DATA, headers=headers)

            assert update_response.status_code == 200, f"Update failed: {update_response.text}"
            response_body = update_response.json()
            assert response_body["success"] is True, "Expected 'success' to be True"
            assert response_body["user"]["name"] == UPDATED_USER_DATA["name"], "Name mismatch"
            assert response_body["user"]["email"] == UPDATED_USER_DATA["email"], "Email mismatch"

        with allure.step("Восстановление исходных данных пользователя"):
            restore_response = requests.patch(
                UPDATE_URL,
                json={"name": NEW_USER["name"], "email": NEW_USER["email"]},
                headers=headers
            )
            assert restore_response.status_code == 200, f"Restore failed: {restore_response.text}"
            restore_body = restore_response.json()

            assert restore_body["success"] is True, "Expected 'success' to be True during restore"
            assert restore_body["user"]["name"] == NEW_USER["name"], "Restored name mismatch"
            assert restore_body["user"]["email"] == NEW_USER["email"], "Restored email mismatch"

    @allure.title("Попытка обновления данных пользователя без авторизации")
    @allure.description("Тест проверяет, что сервер возвращает ошибку при попытке обновления данных пользователя без авторизации.")
    def test_update_user_without_auth(self):
        """Тест обновления данных пользователя без авторизации."""
        with allure.step("Отправка запроса на обновление данных без токена"):
            update_response = requests.patch(UPDATE_URL, json=UPDATED_USER_DATA)

        with allure.step("Проверка ответа сервера"):
            assert update_response.status_code == 401, f"Unexpected status code: {update_response.status_code}"
            response_body = update_response.json()
            assert response_body["success"] is False, "Expected 'success' to be False"
            assert response_body["message"] == "You should be authorised", (
                f"Unexpected message: {response_body['message']}"
            )