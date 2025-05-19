import pytest

from flask.testing import FlaskClient

from app.models import Client, Parking


@pytest.mark.parametrize("url", ["/clients", "/clients/1"])
def test_get_endpoints(client: FlaskClient, test_data: tuple[Client, Parking], url: str) -> None:
    client_obj, _ = test_data
    response = client.get(url.replace("1", str(client_obj.id)))
    assert response.status_code == 200


def test_create_client(client: FlaskClient) -> None:
    response = client.post(
        "/clients",
        json={
            "name": "Test",
            "surname": "User",
            "credit_card": "1111",
            "car_number": "B222BB",
        },
    )
    assert response.status_code == 201


def test_create_parking(client: FlaskClient) -> None:
    response = client.post(
        "/parkings",
        json={
            "address": "Lenina 1",
            "opened": True,
            "count_places": 10,
            "count_available_places": 10,
        },
    )
    assert response.status_code == 201


@pytest.mark.parking
def test_enter_parking(client: FlaskClient, test_data: tuple[Client, Parking]) -> None:
    client_obj, parking_obj = test_data
    response = client.post(
        "/client_parkings",
        json={"client_id": client_obj.id, "parking_id": parking_obj.id},
    )
    assert response.status_code == 200


@pytest.mark.parking
def test_exit_parking(client: FlaskClient, test_data: tuple[Client, Parking]) -> None:
    client_obj, parking_obj = test_data
    client.post(
        "/client_parkings",
        json={"client_id": client_obj.id, "parking_id": parking_obj.id},
    )
    response = client.delete(
        "/client_parkings",
        json={"client_id": client_obj.id, "parking_id": parking_obj.id},
    )
    assert response.status_code == 200
