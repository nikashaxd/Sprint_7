import allure
import requests
from utilities.urls import Urls


@allure.title("Получение списка заказов")
@allure.description("Проверяем, что список заказов возвращается успешно")
def test_get_orders_list():
    response = requests.get(Urls.GET_ORDERS_URL)

    assert response.status_code == 200
    assert "orders" in response.json()
    assert isinstance(response.json()['orders'], list)
