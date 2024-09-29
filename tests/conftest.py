import pytest
import requests
from utilities.courier_helper import generate_random_string
from utilities.urls import Urls


@pytest.fixture
def create_and_delete_courier():
    courier_data = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

    response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)
    assert response.status_code == 201

    yield courier_data

    login_payload = {
        "login": courier_data['login'],
        "password": courier_data['password']
    }

    login_response = requests.post(Urls.LOGIN_COURIER_URL, json=login_payload)
    assert login_response.status_code == 200

    courier_id = login_response.json()['id']

    delete_response = requests.delete(f"{Urls.DELETE_COURIER_URL}/{courier_id}")
    assert delete_response.status_code == 200


@pytest.fixture
def courier_data_fields():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
