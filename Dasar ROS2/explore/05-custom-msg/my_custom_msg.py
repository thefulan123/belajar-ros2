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

# (1) Python dataclass — mensimulasikan custom message ROS2.
# Di ROS2 sesungguhnya, kita pakai file .msg + colcon build.
# Tapi untuk pembelajaran, dataclass lebih sederhana.
from dataclasses import dataclass
from typing import List


@dataclass
class SensorData:
    # (2) @dataclass — decorator Python yang otomatis membuat constructor.
    # Field-field di bawah jadi parameter constructor secara otomatis.
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
    temperature: float    # (3) Suhu dalam Celsius, tipe float.
    humidity: float       # (4) Kelembaban dalam %, tipe float.
    pressure: float       # (5) Tekanan dalam hPa, tipe float.
    unit: str = "Celsius" # (6) Satuan suhu, default "Celsius".

    def to_dict(self):
        # (7) Method untuk mengubah objek ke dictionary (serialisasi).
        # Berguna untuk dikirim sebagai JSON lewat topic String.
        """Ubah ke dictionary untuk serialisasi."""
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'unit': self.unit,
        }

    @classmethod
    def from_dict(cls, data: dict):
        # (8) Class method untuk membuat objek dari dictionary (deserialisasi).
        # @classmethod — method yang dipanggil langsung dari class, bukan instance.
        # Berguna saat menerima JSON dari topic.
        """Buat dari dictionary."""
        return cls(
            temperature=data['temperature'],
            humidity=data['humidity'],
            pressure=data['pressure'],
            unit=data.get('unit', 'Celsius'),
        )

    def __str__(self):
        # (9) Method untuk representasi string yang rapi.
        return (f"SensorData("
                f"temp={self.temperature:.1f}{self.unit}, "
                f"hum={self.humidity:.1f}%, "
                f"press={self.pressure:.1f}hPa)")


@dataclass
class RobotStatus:
    # (10) Class dataclass kedua — untuk status robot.
    """
    Custom message: status robot.
    """
    battery_level: float       # (11) Persentase baterai 0-100.
    is_moving: bool            # (12) Apakah robot sedang bergerak.
    linear_speed: float        # (13) Kecepatan linier (m/s).
    angular_speed: float       # (14) Kecepatan angular (rad/s).
    error_codes: List[int] = None  # (15) Daftar kode error (opsional).

    def __str__(self):
        # (16) Representasi string.
        moving = "bergerak" if self.is_moving else "diam"
        errors = f", error={self.error_codes}" if self.error_codes else ""
        return (f"RobotStatus("
                f"baterai={self.battery_level:.0f}%, "
                f"status={moving}{errors})")


# (17) Contoh penggunaan — hanya jalan jika file dieksekusi langsung.
if __name__ == '__main__':
    # (18) Membuat objek SensorData dengan data contoh.
    sensor = SensorData(
        temperature=28.5,
        humidity=65.0,
        pressure=1013.2
    )
    print(sensor)  # (19) Cetak: SensorData(temp=28.5Celsius, hum=65.0%, press=1013.2hPa)

    # (20) Membuat objek RobotStatus dengan data contoh.
    robot = RobotStatus(
        battery_level=85.0,
        is_moving=True,
        linear_speed=0.5,
        angular_speed=0.0
    )
    print(robot)  # (21) Cetak: RobotStatus(baterai=85%, status=bergerak)
