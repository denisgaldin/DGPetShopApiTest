import allure
import jsonschema
import requests
from .schemas.pet_schemas import PET_SCHEMA
from .schemas.pet_shemas_full_date import PET_SCHEMA_FULL_DATE

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 200, "Код ответа не соответствует ожидаемому"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ответа не соответствует ожидаемому"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 404, "Код ответа не соответствует ожидаемому"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ответа не соответствует ожидаемому"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статус-кода"):
            assert response.status_code == 404, "Код ответа не соответствует ожидаемому"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ответа не соответствует ожидаемому"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на созданте питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации JSON схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "имя питомнца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "статус питомнца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_full_date(self):
        with allure.step("Подготовка полных данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }

        with allure.step("Отправка запроса на созданте питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации JSON схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA_FULL_DATE)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "имя питомца не совпадает с ожидаемым"
            assert response_json["category"] == payload["category"], "категория питомца не совпадает с ожидаемым"
            assert response_json["photoUrls"] == payload["photoUrls"], "Ссылка на фотографию питомца не совпадает с ожидаемым"
            assert response_json["tags"] == payload["tags"], "Тэги питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "статус питомнца не совпадает с ожидаемым"
