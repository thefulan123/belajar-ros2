#!/usr/bin/env python3
"""
gas_alarm.py — alarm kebocoran gas

Bunyikan buzzer (topic /buzzer) jika kadar gas berbahaya.

Cara pakai:
  python3 gas_alarm.py
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
from std_msgs.msg import Int32     # Tipe pesan Int32 — untuk frekuensi buzzer

class GasAlarm(Node):                                    # Node ROS2 — alarm kebocoran gas
    def __init__(self):
        super().__init__('gas_alarm')                    # Inisialisasi node dengan nama "gas_alarm"
        self.pub = self.create_publisher(Int32, 'buzzer', 10)  # Publisher ke topic "buzzer"
        self.sub = self.create_subscription(             # Subscribe ke topic "gas"
            Int32, 'gas', self.cb_gas, 10)
        self.threshold = 70                               # Threshold: jika gas > 70%, bunyikan alarm
        print(f"Gas alarm aktif. Threshold: {self.threshold}")

    def cb_gas(self, msg):                               # Callback — dipanggil saat ada data gas
        if msg.data > self.threshold:                    # Jika kadar gas melebihi threshold
            buzzer_msg = Int32()
            buzzer_msg.data = 2000                       # Frekuensi alarm 2000 Hz
            self.pub.publish(buzzer_msg)                 # Kirim perintah ke buzzer
            print(f"GAS TERDETEKSI! Level: {msg.data}%")
        else:                                            # Jika aman
            buzzer_msg = Int32()
            buzzer_msg.data = 0                          # 0 = matikan buzzer
            self.pub.publish(buzzer_msg)

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = GasAlarm()                               # Buat instance node GasAlarm
    try:
        rclpy.spin(node)                            # Loop forever — proses callback terus
    except KeyboardInterrupt:                       # Tangani Ctrl+C
        pass
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
