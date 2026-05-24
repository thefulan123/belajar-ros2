#!/usr/bin/env python3
"""
dht_display.py — tampilkan suhu & kelembapan di LCD

Subscribe DHT (explore/05) → publish ke LCD.

Cara pakai:
  python3 dht_display.py
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
from std_msgs.msg import Float64, String

class DHTDisplay(Node):
    def __init__(self):
        # super().__init__(): buat node 'dht_display'.
        super().__init__('dht_display')
        # Publisher ke topic /lcd (String) — untuk LCD I2C.
        self.pub = self.create_publisher(String, 'lcd', 10)
        # State suhu dan kelembapan terbaru.
        self.suhu = 0.0
        self.kelembapan = 0.0
        # Subscribe ke topic /suhu dan /kelembapan (dari node DHT).
        self.create_subscription(Float64, 'suhu', self.cb_suhu, 10)
        self.create_subscription(Float64, 'kelembapan', self.cb_kelembapan, 10)
        # Timer 2 detik: update LCD secara periodik.
        self.timer = self.create_timer(2.0, self.update_display)
        print("DHT Display aktif. Update LCD tiap 2 detik.")

    def cb_suhu(self, msg):
        # Simpan nilai suhu terbaru.
        self.suhu = msg.data

    def cb_kelembapan(self, msg):
        # Simpan nilai kelembapan terbaru.
        self.kelembapan = msg.data

    def update_display(self):
        # Format teks untuk LCD 2 baris.
        baris1 = f"Suhu: {self.suhu:.1f}C"
        baris2 = f"RH: {self.kelembapan:.1f}%"
        lcd_msg = String()
        # Gabung dengan \n sebagai pemisah baris.
        lcd_msg.data = f"{baris1}\n{baris2}"
        # Kirim ke topic /lcd → akan ditampilkan oleh lcd_i2c.ino.
        self.pub.publish(lcd_msg)

def main():
    rclpy.init()
    node = DHTDisplay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
