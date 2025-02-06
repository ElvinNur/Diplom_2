import requests
import pytest
import allure
from config import GET_ORDERS_URL

class TestGetUserOrders:

    @allure.title("Получение заказов с авторизацией")
    @allure.description("Тест проверяет успешное получение заказов авторизованного пользователя.")
    def test_get_orders_with_auth(self, headers):
        """Тест получения заказов с авторизацией."""
        with allure.step("Отправка запроса на получение заказов"):
            response = requests.get(GET_ORDERS_URL, headers=headers)

        with allure.step("Проверка ответа от сервера"):
            # Проверяем успешный ответ
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
            response_body = response.json()

            # Проверяем данные в ответе
            assert response_body["success"] is True, "Expected 'success' to be True"
            assert "orders" in response_body, "Key 'orders' not found in response"
            assert isinstance(response_body["orders"], list), "'orders' is not a list"
            assert "total" in response_body, "Total orders should be"
            assert "totalToday" in response_body, "Total orders today should be"

    @allure.title("Получение заказов без авторизации")
    @allure.description("Тест проверяет, что сервер возвращает ошибку при запросе заказов без авторизации.")
    def test_get_orders_without_auth(self):
        """Тест получения заказов без авторизации."""
        with allure.step("Отправка запроса на получение заказов без токена авторизации"):
            response = requests.get(GET_ORDERS_URL)

        with allure.step("Проверка ответа от сервера"):
            # Проверяем, что сервер вернул ошибку
            assert response.status_code == 401, f"Unexpected status code: {response.status_code}"
            response_body = response.json()

            # Проверяем тело ответа
            assert response_body["success"] is False, "Expected 'success' to be False"
            assert response_body["message"] == "You should be authorised", (
                f"Unexpected message: {response_body['message']}"
            )