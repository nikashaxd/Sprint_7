import allure
import pytest
import requests
from utilities.courier_helper import generate_random_string
from utilities.urls import Urls


@allure.title("Создание курьера")
@allure.description("Тест на успешное создание нового курьера через API")
def test_create_courier():
    courier_data = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

    response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)

    assert response.status_code == 201
    assert response.json() == {"ok": True}


@allure.title("Создание дубликата курьера")
@allure.description("Проверяем, что система не позволит создать двух курьеров с одинаковыми данными")
def test_create_duplicate_courier(create_and_delete_courier):
    courier_data = create_and_delete_courier

    payload = {
        "login": courier_data['login'],
        "password": courier_data['password'],
        "firstName": courier_data['firstName']
    }

    response = requests.post(Urls.CREATE_COURIER_URL, json=payload)

    assert response.status_code == 409
    assert response.json().get("message") == "Этот логин уже используется"


@allure.title("Создание курьера без обязательных полей")
@allure.description("Проверяем, что система вернёт ошибку, если не переданы обязательные поля")
def test_create_courier_missing_fields():
    payload = {
        "login": "",
        "password": "",
        "firstName": ""
    }

    response = requests.post(Urls.CREATE_COURIER_URL, json=payload)

    assert response.status_code == 400
    assert response.json().get("message") == "Недостаточно данных для создания учетной записи"


@allure.title("Создание курьера с пропуском обязательных полей")
@allure.description("Проверяем, что система вернёт ошибку, если не переданы обязательные поля")
@pytest.mark.parametrize("missing_field", [["login"], ["password"]])
def test_create_courier_missing_field(missing_field, courier_data_fields):
    list(map(courier_data_fields.pop, missing_field))

    response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data_fields)

    assert response.status_code == 400
    assert response.json().get("message") == "Недостаточно данных для создания учетной записи"
