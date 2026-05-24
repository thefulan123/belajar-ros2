#!/usr/bin/env python3
"""
dashboard.py — dashboard monitoring robot

Menampilkan semua data sensor dari robot di terminal secara real-time.
Menggunakan clear screen setiap 0.5 detik untuk efek dashboard live.

Cara pakai:
  python3 dashboard.py
"""


# ═══════════════════════════════════════════════════════════════
# PENJELASAN DATA STRUCTURE — rclpy (ROS2 Python)
# ═══════════════════════════════════════════════════════════════
#
# Berikut adalah data structure / objek ROS2 yang dipakai:
#
# 1. rclpy
#    - Library utama ROS2 Python. WAJIB untuk semua program.
#    - rclpy.init() = inisialisasi, rclpy.spin() = loop utama.
#
# 2. Node (dari rclpy.node)
#    - Kelas dasar node ROS2. Setiap node punya nama unik.
#    - Bisa memiliki publisher, subscriber, timer, service, dll.
#
# 3. Publisher (create_publisher())
#    - Mengirim data ke topic ROS2 secara periodik.
#    - Parameter: tipe_msg, nama_topic, queue_size.
#    - Method: publish(msg) — kirim ke semua subscriber.
#
# 4. Subscription (create_subscription())
#    - Menerima data dari topic ROS2.
#    - Parameter: tipe_msg, nama_topic, callback, qos.
#    - Callback dipanggil otomatis saat ada data masuk.
#
# 5. Timer (create_timer())
#    - Eksekusi fungsi callback secara periodik.
#    - Parameter: interval_detik, callback_function.
#
# 6. Callback
#    - Fungsi yang dipanggil OTOMATIS oleh ROS2.
#    - Bisa dari: timer, subscriber, service, action.
#    - Tidak dipanggil langsung oleh kode kita.
#
# 7. Tipe pesan standar:
#    - std_msgs.msg.Bool     → bool (true/false)
#    - std_msgs.msg.Int32    → int (angka bulat)
#    - std_msgs.msg.Float64  → float (angka desimal)
#    - std_msgs.msg.String   → string (teks)
# ═══════════════════════════════════════════════════════════════

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
