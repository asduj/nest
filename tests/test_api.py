from starlette.testclient import TestClient
from tests.test_grouping import input_data, output_data
from server import app
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

client = TestClient(app)


def test_api__ok():
    response = client.post(
        '/nest/',
        auth=('admin', 'admin'),
        json=input_data,
        params={'keys': ['currency', 'country', 'city']}
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == output_data


def test_api__unauthorized():
    response = client.post(
        '/nest/',
        json=input_data,
        params={'keys': ['currency', 'country', 'city']}
    )

    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_api__bad_params_format():
    response = client.post(
        '/nest/',
        auth=('admin', 'admin'),
        json=input_data,
        params={'keys': str(['currency', 'country', 'city'])}
    )

    assert response.status_code == HTTP_400_BAD_REQUEST


def test_api__missing_keys_param():
    response = client.post(
        '/nest/',
        auth=('admin', 'admin'),
        json=input_data,
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_api__missing_body():
    response = client.post(
        '/nest/',
        auth=('admin', 'admin'),
        params={'keys': ['currency', 'country', 'city']}
    )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

