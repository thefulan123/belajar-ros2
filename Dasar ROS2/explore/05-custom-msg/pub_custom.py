#!/usr/bin/env python3
# ============================================================
# pub_custom.py — Publisher dengan Custom Message
#
# Mengirim data SensorData ke topic /sensor_data.
# Karena kita belum build .msg file, kita kirim sebagai JSON string.
# (Di ROS2 sungguhan, kita pakai .msg yang dibuild)
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
# 3. Publisher (create_publisher())
#    - Mengirim data ke topic ROS2 secara periodik.
#    - Di sini: publish String yang berisi JSON.
#
# 4. std_msgs.msg.String
#    - Tipe pesan standar ROS2 untuk teks.
#    - Digunakan sebagai "wrapper" untuk data JSON.
#
# 5. json (Python standard library)
#    - Bukan ROS2 — library Python untuk serialisasi data.
#    - json.dumps() = ubah dict/dataclass ke string JSON.
#    - Sementara custom message belum di-build via colcon.
#
# 6. SensorData (dataclass)
#    - Custom message simulasi dari my_custom_msg.py.
#    - Field: temperature, humidity, pressure.
# ═══════════════════════════════════════════════════════════════

import json  # (1) Library JSON — untuk serialisasi data ke format teks.
import rclpy  # (2) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (3) Kelas dasar Node untuk membuat node ROS2.
from std_msgs.msg import String  # (4) Tipe String standar — kita kirim JSON sebagai string.
from my_custom_msg import SensorData  # (5) Custom message kita (dataclass).


class CustomPubNode(Node):
    # (6) Semua node ROS2 HARUS mewarisi class Node.
    def __init__(self):
        # (7) Panggil constructor parent dengan nama node UNIK.
        super().__init__('custom_pub_node')
        # (8) Publisher ke topic '/sensor_data' dengan tipe String (JSON).
        self.publisher = self.create_publisher(String, 'sensor_data', 10)
        # (9) Timer — kirim data setiap 1 detik.
        self.timer = self.create_timer(1.0, self.timer_callback)
        # (10) Log bahwa node siap.
        self.get_logger().info('Publisher custom message siap!')

    def timer_callback(self):
        # (11) CALLBACK TIMER — dipanggil setiap 1 detik.
        # Buat data custom
        import random  # (12) Random — untuk simulasi data sensor bervariasi.
        sensor = SensorData(
            temperature=round(random.uniform(20.0, 35.0), 1),  # (13) Suhu acak 20-35°C.
            humidity=round(random.uniform(40.0, 80.0), 1),     # (14) Kelembaban acak 40-80%.
            pressure=round(random.uniform(1000.0, 1020.0), 1)  # (15) Tekanan acak 1000-1020 hPa.
        )

        # (16) Kirim sebagai JSON string (karena kita belum punya .msg file).
        # json.dumps() mengubah dictionary → string JSON.
        msg = String()
        msg.data = json.dumps(sensor.to_dict())
        # (17) Publikasikan ke topic /sensor_data.
        self.publisher.publish(msg)
        # (18) Log data yang dikirim.
        self.get_logger().info(f'Mengirim: {sensor}')


def main():
    # (19) rclpy.init() — inisialisasi ROS2 (WAJIB).
    rclpy.init()
    node = CustomPubNode()
    try:
        # (20) rclpy.spin(node) — loop utama.
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nPublisher dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
