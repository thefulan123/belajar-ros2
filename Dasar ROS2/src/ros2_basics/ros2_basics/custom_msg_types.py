from dataclasses import dataclass
from typing import List


@dataclass
class SensorData:
    """Custom message: data sensor suhu, kelembaban, tekanan."""
    temperature: float
    humidity: float
    pressure: float
    unit: str = "Celsius"

    def to_dict(self):
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'unit': self.unit,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            temperature=data['temperature'],
            humidity=data['humidity'],
            pressure=data['pressure'],
            unit=data.get('unit', 'Celsius'),
        )
