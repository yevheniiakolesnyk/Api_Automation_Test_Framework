import random
import json
import pytest
from src.services import CarApiService

car_api = CarApiService()


def test_create_new_car(sign_up_response, headers):
    payload = json.dumps({
        "carBrandId": 1,
        "carModelId": 1,
        "mileage": 1
    })
    headers['Content-Type'] = 'application/json'
    response = car_api.create_new_car(body=payload, headers=headers)

    assert response.is_status_code(201)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['carBrandId'] == int(payload.split()[1][0])


def test_get_car_brand(sign_up_response, headers):
    response = car_api.get_car_brand(headers=headers)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'


def test_get_car_brand_by_id(sign_up_response, headers):
    random_id = random.randint(1, 5)
    response = car_api.get_car_brand_by_id(headers=headers, random=random_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['id'] == random_id


def test_get_cars_model(sign_up_response, headers):
    response = car_api.get_cars_model(headers=headers)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'


def test_get_car_model_by_id(sign_up_response, headers):
    random_id = random.randint(1, 23)
    response = car_api.get_car_model_by_id(headers=headers, random=random_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['id'] == random_id


def test_get_current_user_car_by_id(sign_up_response, headers, car_id):
    response = car_api.get_current_user_car_by_id(headers=headers, created_car_id=car_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'


def test_edit_existing_car(sign_up_response, headers, car_id):
    payload = json.dumps({
        "carBrandId": 2,
        "carModelId": 6,
        "mileage": 168223
    })
    headers['Content-Type'] = 'application/json'
    response = car_api.edit_existing_car(body=payload, headers=headers, created_car_id=car_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['mileage'] == int(payload.split()[5][:-1])
    assert response.get_field('data')['carBrandId'] == int(payload.split()[1][:-1])


def test_delete_existing_car(sign_up_response, headers, car_id):
    response = car_api.delete_existing_car(headers=headers, created_car_id=car_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
