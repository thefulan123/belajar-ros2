from dataclasses import dataclass  # (1) Decorator untuk membuat data class Python.
from typing import List  # (2) Type hint untuk list.


@dataclass
class SensorData:
    # (3) @dataclass — otomatis membuat constructor dari field.
    # Field: temperature, humidity, pressure, unit.
    """Custom message: data sensor suhu, kelembaban, tekanan."""
    temperature: float  # (4) Suhu dalam Celsius.
    humidity: float     # (5) Kelembaban dalam %.
    pressure: float     # (6) Tekanan dalam hPa.
    unit: str = "Celsius"  # (7) Satuan suhu, default "Celsius".

    def to_dict(self):
        # (8) Serialisasi objek → dictionary (untuk JSON).
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'unit': self.unit,
        }

    @classmethod
    def from_dict(cls, data: dict):
        # (9) Deserialisasi dictionary → objek (dari JSON).
        # @classmethod — dipanggil langsung dari class, bukan instance.
        return cls(
            temperature=data['temperature'],
            humidity=data['humidity'],
            pressure=data['pressure'],
            unit=data.get('unit', 'Celsius'),
        )
