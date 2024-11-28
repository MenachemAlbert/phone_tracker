from dataclasses import dataclass


@dataclass
class Device:
    device_id: str
    name:str
    brand: str
    model: str
    os: str
    latitude: float
    longitude: float
    altitude_meters: float
    accuracy_meters: float
