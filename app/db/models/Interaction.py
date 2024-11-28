from dataclasses import dataclass


@dataclass
class Interaction:
    method: str
    bluetooth_version: str
    signal_strength_dbm: int
    distance_meters: float
    duration_seconds: int
    timestamp: str
