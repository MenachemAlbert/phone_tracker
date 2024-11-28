from flask import Blueprint, request, jsonify

from app.db.models.Interaction import Interaction
from app.db.models.device import Device
from app.repository.device_repository import insert_device, create_device_interaction, get_device_by_id, \
    get_bluetooth_connected_devices, get_devices_connected_stronger_than_60, count_connected_devices, check_connection, \
    get_most_recent_interaction

phone_blueprint = Blueprint("phone_tracker", __name__)


@phone_blueprint.route("/", methods=['POST'])
def get_interaction():
    devices_data = request.json.get('devices')
    for device_data in devices_data:
        location_data = device_data.get('location')
        device_id = device_data.get('id')
        if get_device_by_id(device_id) is None:
            device = Device(
                device_id=device_id,
                name=device_data.get('name'),
                brand=device_data.get('brand'),
                model=device_data.get('model'),
                os=device_data.get('os'),
                latitude=location_data.get('latitude'),
                longitude=location_data.get('longitude'),
                altitude_meters=location_data.get('altitude_meters'),
                accuracy_meters=location_data.get('accuracy_meters')
            )
            res = insert_device(device)
            print(f"Device created: {res}")
        else:
            print(f"Device with id : {device_id} already exists")
    interaction_data = request.json.get('interaction')
    interaction = Interaction(
        from_device_id=interaction_data.get('from_device'),
        to_device_id=interaction_data.get('to_device'),
        method=interaction_data.get('method'),
        bluetooth_version=interaction_data.get('bluetooth_version'),
        signal_strength_dbm=interaction_data.get('signal_strength_dbm'),
        distance_meters=interaction_data.get('distance_meters'),
        duration_seconds=interaction_data.get('duration_seconds'),
        timestamp=interaction_data.get('timestamp'),
    )
    res_interaction = create_device_interaction(interaction)
    print(res_interaction)
    return jsonify({'status': 'success'}), 200


@phone_blueprint.route("/bluetooth_connections", methods=['GET'])
def get_bluetooth_connections():
    try:
        connections = get_bluetooth_connected_devices()
        return jsonify({"status": "success", "connections": connections}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@phone_blueprint.route("/devices_connected_stronger_than_60", methods=['GET'])
def connected_stronger_than_60():
    try:
        connections = get_devices_connected_stronger_than_60()
        return jsonify({"status": "success", "connections": connections}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@phone_blueprint.route("/count_connected_devices", methods=["GET"])
def get_count_connected_devices():
    try:
        device_id = request.json.get('device_id')
        connected_devices_count = count_connected_devices(device_id)
        return jsonify({"device_id": device_id, "connected_devices": connected_devices_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@phone_blueprint.route("/check_connection", methods=["GET"])
def check_devices_connection():
    device_id1 = request.json.get('device_id1')
    device_id2 = request.json.get('device_id2')
    if not get_device_by_id(device_id1) or not get_device_by_id(device_id2):
        return "one or mor devices not exists", 400
    try:
        is_connected = check_connection(device_id1, device_id2)
        return jsonify({"device_id1": device_id1, "device_id2": device_id2, "is_connected": is_connected}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@phone_blueprint.route("/most_recent_interaction", methods=["GET"])
def most_recent_interaction():
    device_id = request.json.get('device_id')
    try:
        res = get_most_recent_interaction(device_id)
        if res is None:
            return jsonify({"message": "No interactions found for the specified device"}), 404
        return jsonify({
            "device_id": device_id,
            "most_recent_interaction": res["interaction_datetime"].strftime("%Y-%m-%dT%H:%M:%S")}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
