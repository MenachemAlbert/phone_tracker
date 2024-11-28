from app.db.database import driver
from app.db.models.Interaction import Interaction
from app.db.models.device import Device


def get_device_by_id(device_id):
    with driver.session() as session:
        query = """
        match (d:Device{device_id:$device_id}) return d
        """
        params = {
            "device_id": device_id
        }
        res = session.run(query, params).single()
        return res if res else None


def insert_device(device: Device):
    with driver.session() as session:
        query = """
        CREATE (d:Device {
            device_id: $device_id,
            name: $name,
            brand: $brand,
            model: $model,
            os: $os,
            latitude: $latitude,
            longitude: $longitude,
            altitude_meters: $altitude_meters,
            accuracy_meters: $accuracy_meters
        }) RETURN d
        """
        params = {
            "device_id": device.device_id,
            "name": device.name,
            "brand": device.brand,
            "model": device.model,
            "os": device.os,
            "latitude": device.latitude,
            "longitude": device.longitude,
            "altitude_meters": device.altitude_meters,
            "accuracy_meters": device.accuracy_meters
        }
        res = session.run(query, params).single()
        if res:
            return dict(res["d"])
        else:
            return None


def create_device_interaction(interaction: Interaction):
    with driver.session() as session:
        query = """
        MATCH (d1:Device {device_id: $from_device_id})
        MATCH (d2:Device {device_id: $to_device_id})
        MERGE (d1)-[r:INTERACTION{method: $method, bluetooth_version: $bluetooth_version, 
                                           signal_strength_dbm: $signal_strength_dbm, distance_meters: $distance_meters, 
                                           duration_seconds: $duration_seconds, timestamp: $timestamp}]->(d2)
        RETURN d1, d2,r
        """
        params = {
            "from_device_id": interaction.from_device_id,
            "to_device_id": interaction.to_device_id,
            "method": interaction.method,
            "bluetooth_version": interaction.bluetooth_version,
            "signal_strength_dbm": interaction.signal_strength_dbm,
            "distance_meters": interaction.distance_meters,
            "duration_seconds": interaction.duration_seconds,
            "timestamp": interaction.timestamp
        }
        res = session.run(query, params).single()
        return res