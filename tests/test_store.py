from http.client import responses

import allure
import jsonschema
import requests
import pytest
from .schemas.store_schemas import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_add_pet(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещения заказа"):
            response = requests.post(f"{BASE_URL}/store/order", json=payload)

        with allure.step("Проверка статуса ответа и валидации JSON схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), STORE_SCHEMA)

    @allure.title("Получение информации о заказе по ID")
    def test_get_by_id(self, create_order):
        with allure.step("Отправка запроса на получение заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение ID заказа"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            assert response.json()["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_order(self, create_order):
        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/{create_order['id']}")

        with allure.step("Проверка статуса ответа и удаление заказа"):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step("Отправка запроса на получение информации об заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{create_order['id']}")

        with allure.step("Проверка статуса ответа и данных о заказе"):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение несуществующего заказа"):
            resource = requests.get(f"{BASE_URL}/store/order/{9999}")

        with allure.step("Проверка статуса ответа о несуществующем заказе"):
            assert resource.status_code == 404, 'Код ответа не совпал с ожидаемым'

    @allure.title("Получение инвентаря магазина")
    @pytest.mark.parametrize(
        "expected_status, expected_count",
        [
            ("approved", 57),
            ("delivered", 50)
        ]
    )
    def test_get_inventory_store(self, expected_status, expected_count):
        with allure.step(f"Отправка запроса на получение данных об инвентаре магазина"):
            response = requests.get(f"{BASE_URL}/store/inventory")

            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step("Проверка формата ответа и данных"):
            inventory_data = response.json()

        assert isinstance(inventory_data, dict), "Ответ не является словарем"

        expected_keys = ["approved", "delivered"]
        for key in expected_keys:
            assert key in inventory_data, f"Ключ {key} отсутствует в ответе"
            assert isinstance(inventory_data[key], int), f"Значение для {key} не является числом"
