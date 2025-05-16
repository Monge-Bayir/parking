import pytest
from app import create_app, db
from app.models import Client, Parking, ClientParking
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_data(app):
    with app.app_context():
        client = Client(name="Ivan", surname="Ivanov", credit_card="123456", car_number="A123BC")
        parking = Parking(address="Main St", opened=True, count_places=10, count_available_places=10)
        db.session.add_all([client, parking])
        db.session.commit()
        return client, parking
