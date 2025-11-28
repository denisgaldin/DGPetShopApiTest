import allure
import jsonschema
import requests
from .schemas.store_schemas import STORE_ORDER_SCHEMA
from .schemas.store_schemas import STORE_INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_place_order(self):
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
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации JSON схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), STORE_ORDER_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json["id"] == payload["id"], "id заказа не совпадает с ожидаемым"
            assert response_json["petId"] == payload["petId"], "id питомца не совпадает с ожидаемым"
            assert response_json["quantity"] == payload["quantity"], "Количество  не совпадает с ожидаемым"
            assert response_json["status"] == payload[
                "status"], "Статус заказа не совпадает с ожидаемым"
            assert response_json["complete"] == payload["complete"], "Готовность заказа совпадает с ожидаемым"

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
    def test_get_inventory_store(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации JSON схемы"):
            assert response.status_code == 200
            jsonschema.validate(instance=response.json(), schema=STORE_INVENTORY_SCHEMA)
