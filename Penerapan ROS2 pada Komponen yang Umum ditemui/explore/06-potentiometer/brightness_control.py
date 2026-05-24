#!/usr/bin/env python3
"""
brightness_control.py — kontrol LED brightness via potensiometer

Mapping:
  Potensio 0-100 → LED brightness (Bool, threshold 50)

Cara pakai:
  python3 brightness_control.py
  # Putar potensio untuk nyalakan/matikan LED
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
from std_msgs.msg import Int32     # Tipe pesan Int32 — menerima nilai potensiometer
from std_msgs.msg import Bool      # Tipe pesan Bool — mengirim perintah ke LED

class BrightnessControl(Node):                           # Node ROS2 — kontrol LED berdasarkan potensiometer
    def __init__(self):
        super().__init__('brightness_control')           # Inisialisasi node dengan nama "brightness_control"
        self.pub = self.create_publisher(Bool, 'led', 10)  # Publisher ke topic "led" (ON/OFF)
        self.sub = self.create_subscription(             # Subscribe ke topic "potensiometer"
            Int32, 'potensiometer', self.cb_pot, 10)
        self.last_led_state = None                        # State LED terakhir (untuk deteksi perubahan)
        print("Kontrol LED via potensiometer. Threshold: 50%")

    def cb_pot(self, msg):                               # Callback — dipanggil saat ada nilai potensiometer
        value = msg.data                                  # Nilai potensiometer 0-100
        led_on = value > 50                               # Threshold 50%: > 50 = nyala, <= 50 = mati

        if led_on != self.last_led_state:                 # Hanya publish jika state berubah
            self.last_led_state = led_on
            led_msg = Bool()
            led_msg.data = led_on
            self.pub.publish(led_msg)                     # Kirim perintah ke topic "led"
            print(f"LED: {'ON' if led_on else 'OFF'} (potensio: {value}%)")

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = BrightnessControl()                      # Buat instance node BrightnessControl
    try:
        rclpy.spin(node)                            # Loop forever — proses callback terus
    except KeyboardInterrupt:                       # Tangani Ctrl+C
        pass
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
