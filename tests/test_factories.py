from app import db
from factories.factories import ClientFactory, ParkingFactory


def test_create_client_with_factory(app):
    with app.app_context():
        client = ClientFactory()
        db.session.commit()
        assert client.id is not None


def test_create_parking_with_factory(app):
    with app.app_context():
        parking = ParkingFactory()
        db.session.commit()
        assert parking.count_places == parking.count_available_places
