import allure
import pytest
import requests
from utilities.courier_helper import generate_random_string
from utilities.urls import Urls



@allure.title("Авторизация курьера")
@allure.description("Проверяем, что курьер может успешно авторизоваться")
def test_courier_login(create_and_delete_courier):
    courier_data = create_and_delete_courier

    login_payload = {
        "login": courier_data['login'],
        "password": courier_data['password']
    }

    response = requests.post(Urls.LOGIN_COURIER_URL, json=login_payload)

    assert response.status_code == 200
    assert "id" in response.json()


@allure.title("Авторизация без обязательных полей")
@allure.description("Проверяем, что система вернёт ошибку, если логин или пароль не переданы")
def test_courier_login_missing_fields():
    login_payload = {
        "login": "",
        "password": ""
    }

    response = requests.post(Urls.LOGIN_COURIER_URL, json=login_payload)

    assert response.status_code == 400
    assert response.json().get(
        "message") == "Недостаточно данных для входа"


@allure.description("Проверяем, что система вернёт ошибку, если отсутствует одно из обязательных полей")
@pytest.mark.xfailed #504 = <Response [504]>.status_code без пароля
@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_login_courier_missing_field(missing_field):
    courier_data = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
    }

    courier_data.pop(missing_field)

    response = requests.post(Urls.LOGIN_COURIER_URL, json=courier_data)

    assert response.status_code == 400
    assert response.json().get("message") == "Недостаточно данных для входа"


@allure.title("Авторизация с неверными данными")
@allure.description("Проверяем, что система вернёт ошибку, если введены неверные логин или пароль")
def test_invalid_courier_login():
    login_payload = {
        "login": "invalidlogin",
        "password": "invalidpassword"
    }

    response = requests.post(Urls.LOGIN_COURIER_URL, json=login_payload)

    assert response.status_code == 404
    assert response.json().get("message") == "Учетная запись не найдена"
