from flask import Blueprint, request, jsonify
from .models import db, Client, Parking, ClientParking
from datetime import datetime

bp = Blueprint('api', __name__)

@bp.route('/clients', methods=['GET'])
def get_clients():
    return jsonify([{"id": c.id, "name": c.name} for c in Client.query.all()])

@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    c = Client.query.get_or_404(client_id)
    return jsonify({"id": c.id, "name": c.name, "surname": c.surname})

@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    client = Client(**data)
    db.session.add(client)
    db.session.commit()
    return jsonify({"id": client.id}), 201

@bp.route('/parkings', methods=['POST'])
def create_parking():
    data = request.json
    parking = Parking(**data)
    db.session.add(parking)
    db.session.commit()
    return jsonify({"id": parking.id}), 201

@bp.route('/client_parkings', methods=['POST'])
def enter_parking():
    data = request.json
    parking = Parking.query.get_or_404(data['parking_id'])
    if not parking.opened or parking.count_available_places <= 0:
        return jsonify({"error": "Parking closed or full"}), 400
    client = Client.query.get_or_404(data['client_id'])
    if not client.credit_card:
        return jsonify({"error": "No credit card"}), 400

    parking.count_available_places -= 1
    log = ClientParking(client_id=client.id, parking_id=parking.id, time_in=datetime.now())
    db.session.add(log)
    db.session.commit()
    return jsonify({"status": "entered"}), 200

@bp.route('/client_parkings', methods=['DELETE'])
def exit_parking():
    data = request.json
    log = ClientParking.query.filter_by(client_id=data['client_id'], parking_id=data['parking_id']).first_or_404()
    parking = Parking.query.get_or_404(data['parking_id'])
    client = Client.query.get_or_404(data['client_id'])

    if not client.credit_card:
        return jsonify({"error": "No credit card"}), 400

    log.time_out = datetime.now()
    if log.time_out < log.time_in:
        return jsonify({"error": "Invalid time"}), 400
    parking.count_available_places += 1

    db.session.commit()
    return jsonify({"status": "exited"}), 200