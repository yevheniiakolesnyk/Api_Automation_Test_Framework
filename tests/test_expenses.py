import json
import pytest
import random
import datetime
from src.services import ExpensesApiService

expenses_api = ExpensesApiService()


@pytest.fixture()
def report_date():
    current_date = datetime.datetime.now()
    formatted_date = "{}-{}-{}".format(current_date.year, current_date.month, current_date.day)
    return str(formatted_date)


@pytest.fixture()
def expenses_id(sign_up_response, headers, report_date, car_id):
    random_mileage = random.randint(1, 1000)
    random_liters = random.randint(1, 1000)
    payload = json.dumps({
        "carId": car_id,
        "reportedAt": report_date,
        "mileage": random_mileage,
        "liters": random_liters,
        "totalCost": 11,
        "forceMileage": False
    })
    headers['Content-Type'] = 'application/json'
    response = expenses_api.create_expenses(body=payload, headers=headers)
    return response.get_field('data')['id']


def test_create_expenses(sign_up_response, headers, report_date, car_id):
    random_mileage = random.randint(1, 1000)
    random_liters = random.randint(1, 1000)
    payload = json.dumps({
        "carId": car_id,
        "reportedAt": report_date,
        "mileage": random_mileage,
        "liters": random_liters,
        "totalCost": 11,
        "forceMileage": False
    })
    headers['Content-Type'] = 'application/json'
    response = expenses_api.create_expenses(body=payload, headers=headers)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['mileage'] == random_mileage
    assert response.get_field('data')['liters'] == random_liters
    assert response.get_field('data')['reportedAt'] == report_date


def test_get_all_expenses(sign_up_response, headers):
    response = expenses_api.get_all_expenses(headers=headers)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'


def test_get_expenses_by_id(sign_up_response, headers, expenses_id):
    response = expenses_api.get_expenses_by_id(headers=headers, expenses_id=expenses_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['id'] == expenses_id


def test_edit_expense(sign_up_response, headers, report_date, expenses_id, car_id):
    random_mileage = random.randint(1, 1000)
    random_liters = random.randint(1, 1000)
    payload = json.dumps({
        "carId": car_id,
        "reportedAt": report_date,
        "mileage": random_mileage,
        "liters": random_liters,
        "totalCost": 11,
        "forceMileage": False
    })
    headers['Content-Type'] = 'application/json'
    response = expenses_api.edit_expense(body=payload, headers=headers, expenses_id=expenses_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['id'] == str(expenses_id)
    assert response.get_field('data')['mileage'] == random_mileage
    assert response.get_field('data')['liters'] == random_liters
    assert response.get_field('data')['reportedAt'] == report_date


def test_delete_expense(sign_up_response, headers, expenses_id):
    response = expenses_api.delete_expense(headers=headers, expenses_id=expenses_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['expenseId'] == str(expenses_id)
