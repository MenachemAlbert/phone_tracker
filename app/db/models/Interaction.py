from dataclasses import dataclass


@dataclass
class Interaction:
    from_device_id: str
    to_device_id: str
    method: str
    bluetooth_version: str
    signal_strength_dbm: int
    distance_meters: float
    duration_seconds: int
    timestamp: str
