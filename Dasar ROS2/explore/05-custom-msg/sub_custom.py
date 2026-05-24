#!/usr/bin/env python3
# ============================================================
# sub_custom.py — Subscriber dengan Custom Message
#
# Menerima data SensorData dari topic /sensor_data.
# Parse JSON string kembali ke objek SensorData.
# ============================================================

# ═══════════════════════════════════════════════════════════════
# PENJELASAN DATA STRUCTURE
# ═══════════════════════════════════════════════════════════════
#
# Berikut adalah data structure / objek yang dipakai di file ini:
#
# 1. rclpy
#    - Library utama ROS2 Python. Wajib untuk semua node.
#
# 2. Node
#    - Kelas dasar node ROS2. Setiap node punya nama unik.
#
# 3. Subscription (create_subscription())
#    - Menerima data dari topic ROS2.
#    - Callback dipanggil otomatis saat ada data masuk.
#
# 4. std_msgs.msg.String
#    - Tipe pesan standar ROS2 untuk teks.
#    - Data JSON diterima sebagai String, lalu di-parse.
#
# 5. json (Python standard library)
#    - json.loads() = ubah string JSON ke Python dict.
#    - Dipakai untuk decode data dari publisher.
#
# 6. SensorData (dataclass)
#    - Custom message simulasi dari my_custom_msg.py.
#    - Field: temperature, humidity, pressure.
# ═══════════════════════════════════════════════════════════════

import json  # (1) Library JSON — untuk parsing string JSON ke Python dict.
import rclpy  # (2) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (3) Kelas dasar Node untuk membuat node ROS2.
from std_msgs.msg import String  # (4) Tipe String standar — data diterima sebagai string.
from my_custom_msg import SensorData  # (5) Custom message kita (dataclass) untuk parsing.


class CustomSubNode(Node):
    # (6) Semua node ROS2 HARUS mewarisi class Node.
    def __init__(self):
        # (7) Panggil constructor parent dengan nama node UNIK.
        super().__init__('custom_sub_node')
        # (8) Subscription ke topic /sensor_data dengan tipe String (JSON).
        self.subscription = self.create_subscription(
            String,
            'sensor_data',
            self.listener_callback,
            10
        )
        # (9) Log bahwa node siap.
        self.get_logger().info('Subscriber custom message siap!')

    def listener_callback(self, msg):
        # (10) CALLBACK SUBSCRIPTION — dipanggil SETIAP ada data di /sensor_data.
        # msg.data adalah string JSON dari publisher.
        # Parse JSON string ke Python dict
        data = json.loads(msg.data)
        # (11) json.loads() — mengubah string JSON → dictionary Python.

        # Convert dict ke SensorData
        sensor = SensorData.from_dict(data)
        # (12) SensorData.from_dict() — mengubah dictionary → objek SensorData.

        # (13) Log data sensor yang diterima.
        self.get_logger().info(f'Menerima: {sensor}')

        # (14) Contoh logika bisnis: deteksi suhu tinggi.
        if sensor.temperature > 30.0:
            # (15) get_logger().warn() — level warning (kuning).
            self.get_logger().warn(
                f'Suhu tinggi! {sensor.temperature}°C'
            )


def main():
    # (16) rclpy.init() — inisialisasi ROS2 (WAJIB).
    rclpy.init()
    node = CustomSubNode()
    try:
        # (17) rclpy.spin(node) — loop utama.
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nSubscriber dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
