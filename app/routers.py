from typing import Any, Dict
from flask import Blueprint, jsonify, request, Response as FlaskResponse

from .models import Client, ClientParking, Parking, db

bp = Blueprint("api", __name__)


@bp.route("/clients", methods=["POST"])
def create_client() -> FlaskResponse:
    data: Dict[str, Any] = request.get_json()
    name: str = data["name"]
    client = Client(name=name)
    db.session.add(client)
    db.session.commit()
    return jsonify({"id": client.id, "name": client.name}), 201


@bp.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id: int) -> FlaskResponse:
    client = Client.query.get_or_404(client_id)
    return jsonify({"id": client.id, "name": client.name})


@bp.route("/parkings", methods=["POST"])
def create_parking() -> FlaskResponse:
    data: Dict[str, Any] = request.get_json()
    location: str = data["location"]
    parking = Parking(location=location)
    db.session.add(parking)
    db.session.commit()
    return jsonify({"id": parking.id, "location": parking.location}), 201


@bp.route("/parkings/<int:parking_id>", methods=["GET"])
def get_parking(parking_id: int) -> FlaskResponse:
    parking = Parking.query.get_or_404(parking_id)
    return jsonify({"id": parking.id, "location": parking.location})


@bp.route("/assign", methods=["POST"])
def assign_client_to_parking() -> FlaskResponse:
    data: Dict[str, Any] = request.get_json()
    client_id: int = data["client_id"]
    parking_id: int = data["parking_id"]

    client_parking = ClientParking(client_id=client_id, parking_id=parking_id)
    db.session.add(client_parking)
    db.session.commit()
    return jsonify({"message": "Client assigned to parking"}), 201
