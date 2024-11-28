from flask import Blueprint, request, jsonify

from app.db.models.Interaction import Interaction
from app.db.models.device import Device
from app.repository.device_repository import insert_device, create_device_interaction, get_device_by_id

phone_blueprint = Blueprint("phone_tracker", __name__)


@phone_blueprint.route("/phone_tracker", methods=['POST'])
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
