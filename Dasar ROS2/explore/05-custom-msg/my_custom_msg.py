#!/usr/bin/env python3
# ============================================================
# my_custom_msg.py — Custom Message Type (Python version)
#
# ROS2 punya tipe pesan standar: String, Int32, Twist, dll.
# Tapi kadang kita perlu tipe pesan SENDIRI.
#
# Contoh: data sensor suhu + kelembaban + timestamp.
#
# Di ROS2, custom message didefinisikan dengan file .msg
# dan dibuild dengan colcon. Tapi untuk eksplorasi,
# kita bisa pakai Python dataclass sebagai simulasi.
#
# Cara bikin custom message ROS2 yang bener:
#   1. Buat folder msg/ di package
#   2. Buat file SensorData.msg
#   3. Isi: float32 temperature, float32 humidity, float32 pressure
#   4. Update CMakeLists.txt / package.xml
#   5. colcon build
#   6. import dari package_name.msg import SensorData
# ============================================================

# Python dataclass — mensimulasikan custom message
from dataclasses import dataclass
from typing import List


@dataclass
class SensorData:
    """
    Custom message: data sensor sederhana.
    
    Ini adalah SIMULASI. Cara ROS2 yang benar:
    Buat file SensorData.msg dengan isi:
        float32 temperature
        float32 humidity
        float32 pressure
        string unit
    
    Lalu build dengan colcon.
    """
    temperature: float    # Suhu dalam Celsius
    humidity: float       # Kelembaban dalam %
    pressure: float       # Tekanan dalam hPa
    unit: str = "Celsius"

    def to_dict(self):
        """Ubah ke dictionary untuk serialisasi."""
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'unit': self.unit,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Buat dari dictionary."""
        return cls(
            temperature=data['temperature'],
            humidity=data['humidity'],
            pressure=data['pressure'],
            unit=data.get('unit', 'Celsius'),
        )

    def __str__(self):
        return (f"SensorData("
                f"temp={self.temperature:.1f}{self.unit}, "
                f"hum={self.humidity:.1f}%, "
                f"press={self.pressure:.1f}hPa)")


@dataclass
class RobotStatus:
    """
    Custom message: status robot.
    """
    battery_level: float       # Persentase baterai 0-100
    is_moving: bool            # Apakah sedang bergerak
    linear_speed: float        # Kecepatan linier (m/s)
    angular_speed: float       # Kecepatan angular (rad/s)
    error_codes: List[int] = None  # Daftar error (jika ada)

    def __str__(self):
        moving = "bergerak" if self.is_moving else "diam"
        errors = f", error={self.error_codes}" if self.error_codes else ""
        return (f"RobotStatus("
                f"baterai={self.battery_level:.0f}%, "
                f"status={moving}{errors})")


# Contoh penggunaan (kalau di-run langsung)
if __name__ == '__main__':
    sensor = SensorData(
        temperature=28.5,
        humidity=65.0,
        pressure=1013.2
    )
    print(sensor)

    robot = RobotStatus(
        battery_level=85.0,
        is_moving=True,
        linear_speed=0.5,
        angular_speed=0.0
    )
    print(robot)
