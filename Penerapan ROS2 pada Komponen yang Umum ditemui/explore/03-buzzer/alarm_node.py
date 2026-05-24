#!/usr/bin/env python3
"""
alarm_node.py — contoh node alarm di PC

Bunyikan buzzer dalam pola alarm (3 beep cepat, jeda).

Cara pakai:
  python3 alarm_node.py
  # Buzzer akan bunyi beep tiga kali tiap 2 detik
"""

import rclpy                       # Library ROS2 Python — menghubungkan script ke ROS2
from rclpy.node import Node        # Class Node — membuat node ROS2 di Python
from std_msgs.msg import Int32     # Tipe pesan Int32 (integer) — untuk frekuensi buzzer
import time                        # Library time — untuk delay / sleep

class AlarmNode(Node):                                  # Node ROS2 untuk pola alarm buzzer
    def __init__(self):
        super().__init__('alarm_node')                  # Inisialisasi node dengan nama "alarm_node"
        self.pub = self.create_publisher(Int32, 'buzzer', 10)  # Publisher ke topic "buzzer"

    def beep(self, freq, duration_ms):                  # Method: bunyikan buzzer dengan frekuensi tertentu
        msg = Int32()                                   # Buat objek pesan Int32
        msg.data = freq                                 # Set frekuensi (Hz)
        self.pub.publish(msg)                           # Kirim perintah ke buzzer
        time.sleep(duration_ms / 1000.0)                # Tunggu selama durasi beep

    def silent(self, duration_ms):                      # Method: matikan buzzer
        msg = Int32()
        msg.data = 0                                    # Frekuensi 0 = mati
        self.pub.publish(msg)
        time.sleep(duration_ms / 1000.0)                # Tunggu selama durasi diam

    def run(self):                                      # Method utama — jalankan pola alarm
        print("Alarm aktif! Tekan Ctrl+C untuk stop.")
        try:
            while rclpy.ok():                           # Loop selama ROS2 berjalan
                # 3 beep cepat — pola alarm standar
                for _ in range(3):
                    self.beep(2000, 150)                # Beep 2000Hz selama 150ms
                    self.silent(100)                    # Diam 100ms
                self.silent(1700)                        # Jeda panjang 1,7 detik
        except KeyboardInterrupt:                       # Tangani Ctrl+C
            self.silent(0)                              # Matikan buzzer
            print("Alarm dihentikan")

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = AlarmNode()                              # Buat instance node AlarmNode
    try:
        node.run()                                  # Jalankan pola alarm
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
