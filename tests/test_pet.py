import allure
import requests

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
