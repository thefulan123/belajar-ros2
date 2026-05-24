#!/usr/bin/env python3
"""
auto_light.py — lampu otomatis berdasarkan cahaya

Nyalakan LED (topic /led) jika cahaya < threshold.

Cara pakai:
  python3 auto_light.py
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

import rclpy                       # Library ROS2 Python — menghubungkan script ke ROS2
from rclpy.node import Node        # Class Node — membuat node ROS2 di Python
from std_msgs.msg import Int32, Bool  # Tipe pesan Int32 (cahaya) dan Bool (LED ON/OFF)

class AutoLight(Node):                                  # Node ROS2 — lampu otomatis berdasarkan cahaya
    def __init__(self):
        super().__init__('auto_light')                  # Inisialisasi node dengan nama "auto_light"
        self.pub_led = self.create_publisher(Bool, 'led', 10)  # Publisher ke topic "led"
        self.sub = self.create_subscription(            # Subscribe ke topic "cahaya"
            Int32, 'cahaya', self.cb_cahaya, 10)
        self.threshold = 30                             # Threshold: jika cahaya < 30%, anggap gelap
        print(f"Auto light aktif. Threshold: {self.threshold}")

    def cb_cahaya(self, msg):                           # Callback — dipanggil saat ada data cahaya
        gelap = msg.data < self.threshold               # Bandingkan nilai cahaya dengan threshold
        led_msg = Bool()
        led_msg.data = gelap                            # true = gelap (LED ON), false = terang (LED OFF)
        self.pub_led.publish(led_msg)                   # Kirim perintah ke topic "led"
        status = "GELAP - LED ON" if gelap else "TERANG - LED OFF"
        print(f"Cahaya: {msg.data}% | {status}")

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = AutoLight()                              # Buat instance node AutoLight
    try:
        rclpy.spin(node)                            # Loop forever — proses callback terus
    except KeyboardInterrupt:                       # Tangani Ctrl+C
        pass
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
