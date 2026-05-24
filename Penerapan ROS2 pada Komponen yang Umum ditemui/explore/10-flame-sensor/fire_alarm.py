#!/usr/bin/env python3
"""
fire_alarm.py — sistem alarm kebakaran

Jika api terdeteksi: bunyikan buzzer + nyalakan relay (pompa).
Jika aman: matikan semua.

Cara pakai:
  python3 fire_alarm.py
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
from std_msgs.msg import Bool, Int32  # Tipe pesan: Bool (relay/api) dan Int32 (buzzer)

class FireAlarm(Node):                                   # Node ROS2 — sistem alarm kebakaran
    def __init__(self):
        super().__init__('fire_alarm')                   # Inisialisasi node dengan nama "fire_alarm"
        self.pub_buzzer = self.create_publisher(Int32, 'buzzer', 10)  # Publisher ke topic "buzzer"
        self.pub_relay = self.create_publisher(Bool, 'relay', 10)     # Publisher ke topic "relay" (pompa)
        self.sub = self.create_subscription(             # Subscribe ke topic "api"
            Bool, 'api', self.cb_api, 10)

    def cb_api(self, msg):                               # Callback — dipanggil saat ada status api
        if msg.data:                                     # Jika api terdeteksi
            # Alarm!
            buzzer_msg = Int32()
            buzzer_msg.data = 2500                       # Frekuensi alarm 2500 Hz
            self.pub_buzzer.publish(buzzer_msg)          # Bunyikan buzzer

            relay_msg = Bool()
            relay_msg.data = True
            self.pub_relay.publish(relay_msg)            # Nyalakan pompa (relay ON)
            self.get_logger().warn('KEBAKARAN TERDETEKSI! Alarm + Pompa ON')
        else:                                            # Jika aman
            # Matikan semua
            buzzer_msg = Int32()
            buzzer_msg.data = 0                          # 0 = matikan buzzer
            self.pub_buzzer.publish(buzzer_msg)

            relay_msg = Bool()
            relay_msg.data = False
            self.pub_relay.publish(relay_msg)            # Matikan pompa

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = FireAlarm()                              # Buat instance node FireAlarm
    try:
        rclpy.spin(node)                            # Loop forever — proses callback terus
    except KeyboardInterrupt:                       # Tangani Ctrl+C
        pass
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
