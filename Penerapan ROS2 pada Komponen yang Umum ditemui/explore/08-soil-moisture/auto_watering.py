#!/usr/bin/env python3
"""
auto_watering.py — penyiraman otomatis

Nyalakan pompa (topic /relay) jika tanah kering.
Matikan pompa jika tanah sudah basah.

Cara pakai:
  python3 auto_watering.py
"""

import rclpy                       # Library ROS2 Python — menghubungkan script ke ROS2
from rclpy.node import Node        # Class Node — membuat node ROS2 di Python
from std_msgs.msg import Int32, Bool  # Tipe pesan: Int32 (kelembapan) dan Bool (relay ON/OFF)

class AutoWatering(Node):                                # Node ROS2 — penyiraman tanaman otomatis
    def __init__(self):
        super().__init__('auto_watering')                # Inisialisasi node dengan nama "auto_watering"
        self.pub_relay = self.create_publisher(Bool, 'relay', 10)  # Publisher ke topic "relay" (pompa)
        self.sub = self.create_subscription(             # Subscribe ke topic "kelembapan_tanah"
            Int32, 'kelembapan_tanah', self.cb_soil, 10)
        self.pump_on = False                              # Status pompa (ON/OFF)
        self.kering_threshold = 30                        # Ambang kering: jika < 30% → nyalakan pompa
        self.basah_threshold = 60                         # Ambang basah: jika > 60% → matikan pompa
        print(f"Auto watering aktif. Kering < {self.kering_threshold}, Basah > {self.basah_threshold}")

    def cb_soil(self, msg):                              # Callback — dipanggil saat ada data kelembapan tanah
        nilai = msg.data                                  # Nilai kelembapan 0-100
        if nilai < self.kering_threshold and not self.pump_on:  # Tanah kering dan pompa mati → nyalakan
            self.pump_on = True
            relay_msg = Bool()
            relay_msg.data = True
            self.pub_relay.publish(relay_msg)             # Kirim perintah ON ke relay
            print(f"Tanah kering ({nilai}%) → Pompa ON")
        elif nilai > self.basah_threshold and self.pump_on:    # Tanah basah dan pompa nyala → matikan
            self.pump_on = False
            relay_msg = Bool()
            relay_msg.data = False
            self.pub_relay.publish(relay_msg)             # Kirim perintah OFF ke relay
            print(f"Tanah basah ({nilai}%) → Pompa OFF")

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = AutoWatering()                           # Buat instance node AutoWatering
    try:
        rclpy.spin(node)                            # Loop forever — proses callback terus
    except KeyboardInterrupt:                       # Tangani Ctrl+C
        pass
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
