import requests
import pytest
from jsonschema import validate

from src.schemas import (
    user_schema,
    register_schema,
    create_user_schema,
    update_user_schema,
)

BASE_URL = "https://reqres.in/api"


@pytest.fixture
def test_user():
    response = requests.post(f"{BASE_URL}/users",
                             json={"name": "Testname", "job": "Testjob"},
                             headers={"x-api-key": "reqres-free-v1"})
    assert response.status_code == 201, "Не удалось создать тестового пользователя"
    user_data = response.json()
    return user_data


def test_get_user_success():
    response = requests.get(f"{BASE_URL}/users/2",
                            headers={"x-api-key": "reqres-free-v1"})
    assert response.status_code == 200
    validate(instance=response.json(), schema=user_schema)


def test_get_user_error():
    response = requests.get(f"{BASE_URL}/users/0",
                            headers={"x-api-key": "reqres-free-v1"})
    assert response.status_code == 404


def test_create_user_success():
    response = requests.post(f"{BASE_URL}/users",
                             json={"name": "Testname", "job": "Testjob"},
                             headers={"x-api-key": "reqres-free-v1"})
    assert response.status_code == 201
    validate(instance=response.json(), schema=create_user_schema)


def test_update_user_success(test_user):
    user_id = test_user["id"]

    update_response = requests.put(
        f"{BASE_URL}/users/{user_id}",
        json={"name": "Testnewname", "job": "Testnewjob"},
        headers={"x-api-key": "reqres-free-v1"}
    )
    assert update_response.status_code == 200
    validate(instance=update_response.json(), schema=update_user_schema)
    assert update_response.json().get('name') == "Testnewname"
    assert update_response.json().get('job') == "Testnewjob"


def test_delete_user_success(test_user):
    user_id = test_user["id"]

    delete_response = requests.delete(f"{BASE_URL}/users/{user_id}",
                                      headers={"x-api-key": "reqres-free-v1"})
    assert delete_response.status_code == 204
    assert delete_response.text == ""


def test_register_success():
    response = requests.post(f"{BASE_URL}/register",
                             json={"email": "eve.holt@reqres.in", "password": "pistol"},
                             headers={"x-api-key": "reqres-free-v1"})
    assert response.status_code == 200
    validate(instance=response.json(), schema=register_schema)


def test_register_without_password():
    response = requests.post(f"{BASE_URL}/register",
                             json={"email": "eve.holt@reqres.in"},
                             headers={"x-api-key": "reqres-free-v1"})
    assert response.status_code == 400
    assert response.json().get('error') == 'Missing password'


def test_register_without_email():
    response = requests.post(f"{BASE_URL}/register",
                             json={"password": "pistol"},
                             headers={"x-api-key": "reqres-free-v1"})
    assert response.status_code == 400
    assert response.json().get('error') == 'Missing email or username'