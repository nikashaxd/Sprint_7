import allure
import requests
import pytest
from utilities.urls import Urls


@allure.title("Создание заказа с цветами")
@allure.description("Проверка создания заказа с указанием одного или нескольких цветов")
@pytest.mark.parametrize("colors", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
def test_create_order_with_colors(colors):
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Test Address",
        "metroStation": 4,
        "phone": "+7 999 999 99 99",
        "rentTime": 5,
        "deliveryDate": "2023-01-01",
        "comment": "Test comment",
        "color": colors
    }

    response = requests.post(Urls.CREATE_ORDER_URL, json=payload)

    assert response.status_code == 201
    assert "track" in response.json()
