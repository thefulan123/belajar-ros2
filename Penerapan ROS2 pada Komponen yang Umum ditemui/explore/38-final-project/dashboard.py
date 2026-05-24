#!/usr/bin/env python3
"""
dashboard.py — dashboard monitoring robot

Menampilkan semua data sensor dari robot di terminal secara real-time.
Menggunakan clear screen setiap 0.5 detik untuk efek dashboard live.

Cara pakai:
  python3 dashboard.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Int32, Bool, String
import os
import time

class Dashboard(Node):
    def __init__(self):
        # super().__init__: inisialisasi node ROS2 dengan nama 'dashboard'
        super().__init__('dashboard')

        # ===== STATE VARIABLES =====
        # Menyimpan data sensor terbaru — diupdate oleh subscriber callback
        self.jarak = 0.0       # Jarak dari sensor ultrasonik (cm)
        self.suhu = 0.0        # Suhu dari DHT11 (°C)
        self.gas = 0           # Kadar gas dari MQ-2 (%)
        self.api = False       # Status deteksi api (True = ada api)
        self.status = "MENUNGGU..."  # Status robot (dari robot_monitor)

        # ===== SUBSCRIBERS =====
        # Subscribe ke semua topic yang dipublish oleh robot_monitor node
        self.create_subscription(Float64, 'jarak', self.cb_jarak, 10)
        self.create_subscription(Float64, 'suhu', self.cb_suhu, 10)
        self.create_subscription(Int32, 'gas', self.cb_gas, 10)
        self.create_subscription(Bool, 'api', self.cb_api, 10)
        self.create_subscription(String, 'robot_status', self.cb_status, 10)

        # Timer 0.5 detik — refresh tampilan dashboard
        self.timer = self.create_timer(0.5, self.display)
        # Beri waktu untuk inisialisasi subscriber sebelum display pertama
        time.sleep(0.5)
        self.get_logger().info('Dashboard aktif!')

    # ===== CALLBACK SUBSCRIBER =====
    # Dipanggil setiap kali ada data baru di topic masing-masing
    def cb_jarak(self, msg): self.jarak = msg.data     # Update jarak
    def cb_suhu(self, msg): self.suhu = msg.data       # Update suhu
    def cb_gas(self, msg): self.gas = msg.data          # Update gas
    def cb_api(self, msg): self.api = msg.data          # Update status api
    def cb_status(self, msg): self.status = msg.data    # Update status robot

    def display(self):
        """Callback timer: refresh tampilan dashboard di terminal"""
        # Clear screen: 'clear' untuk Linux/Mac, 'cls' untuk Windows
        os.system('clear' if os.name == 'posix' else 'cls')
        # Tampilkan dashboard dengan format tabel
        print("=" * 50)
        print("       ROBOT MONITORING DASHBOARD")
        print("=" * 50)
        # :6.1f = lebar 6 karakter, 1 desimal
        print(f"  Jarak:       {self.jarak:6.1f} cm")
        print(f"  Suhu:        {self.suhu:6.1f} C")
        # :6d = lebar 6 karakter, integer
        print(f"  Gas:         {self.gas:6d} %")
        # Ternary: tampilkan peringatan jika api terdeteksi
        print(f"  Api:         {'TERDETEKSI!' if self.api else 'Aman'}")
        print(f"  Status:      {self.status}")
        print("=" * 50)
        print("  [Ctrl+C untuk keluar]")

def main():
    # rclpy.init: inisialisasi ROS2
    rclpy.init()
    node = Dashboard()
    try:
        # rclpy.spin: loop utama — terus proses callback
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
