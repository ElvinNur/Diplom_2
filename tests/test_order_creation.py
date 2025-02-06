import requests
import pytest
import allure
from config import ORDER_CREATION_URL
from data import VALID_INGREDIENTS

class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией")
    @allure.description("Тест проверяет успешное создание заказа с авторизацией.")
    def test_create_order_with_auth(self, headers):
        """Тест создания заказа с авторизацией."""
        with allure.step("Подготовка данных для заказа"):
            payload = {"ingredients": VALID_INGREDIENTS}

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(ORDER_CREATION_URL, json=payload, headers=headers)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200, f"Order create failed: {response.text}"
            response_body = response.json()

            assert response_body["success"] is True, "Expected 'success' to be True"
            assert "order" in response_body, "Key 'order' not found in response"
            assert response_body["order"]["number"] > 0, "Order number mismatch"

    @allure.title("Создание заказа без авторизации")
    @allure.description("Тест проверяет, что заказ без авторизации невозможен.")
    def test_create_order_without_auth(self):
        with allure.step("Подготовка данных для заказа"):
            payload = {"ingredients": VALID_INGREDIENTS}

        with allure.step("Отправка запроса на создание заказа без авторизации"):
            response = requests.post(ORDER_CREATION_URL, json=payload)

        with allure.step("Проверка ответа на отсутствие авторизации"):
            assert response.status_code == 401, f"Unexpected status code: {response.status_code}"
            response_body = response.json()

            assert response_body["success"] is False, "Expected 'success' to be False"
            assert response_body["message"] == "You should be authorised", (
                f"Unexpected message: {response_body['message']}"
            )

    @allure.title("Создание заказа с некорректным ингредиентом")
    @allure.description("Тест проверяет, что заказ с некорректным идентификатором ингредиента не может быть создан.")
    def test_create_order_with_invalid_ingredient_hash(self, headers):
        """Тест создания заказа с некорректным ингредиентом."""
        with allure.step("Подготовка данных с некорректным ингредиентом"):
            invalid_ingredient = ["61c0c5a71d1f820ggdd"]
            payload = {"ingredients": invalid_ingredient}

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(ORDER_CREATION_URL, json=payload, headers=headers)

        with allure.step("Проверка ответа на некорректный ингредиент"):
            assert response.status_code == 500, f"Order create failed: {response.text}"

    @allure.title("Создание заказа без указания ингредиентов")
    @allure.description("Тест проверяет, что заказ без указания ингредиентов невозможен.")
    def test_create_order_without_ingredients(self, headers):
        """Тест создания заказа без указания ингредиентов."""
        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            response = requests.post(ORDER_CREATION_URL, headers=headers)

        with allure.step("Проверка ответа на отсутствие ингредиентов"):
            assert response.status_code == 400, f"Order create failed: {response.text}"
            response_body = response.json()

            assert response_body["success"] is False, "Expected 'success' to be False"
            assert response_body["message"] == "Ingredient ids must be provided", (
                f"Unexpected message: {response_body['message']}"
            )

    @allure.title("Создание заказа с одним валидным ингредиентом")
    @allure.description("Тест проверяет успешное создание заказа с одним валидным ингредиентом.")
    def test_create_order_with_specific_ingredient(self, headers):
        """Тест создания заказа с одним валидным ингредиентом."""
        with allure.step("Подготовка данных для заказа"):
            payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(ORDER_CREATION_URL, json=payload, headers=headers)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200, f"Order create failed: {response.text}"
            response_body = response.json()

            assert response_body["success"] is True, "Expected 'success' to be True"
            assert "order" in response_body, "Key 'order' not found in response"
            assert response_body["order"]["number"] > 0, "Order number mismatch"

        