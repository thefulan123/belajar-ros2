#!/usr/bin/env python3
"""
security_light.py — lampu otomatis sensor gerak

Nyalakan LED jika gerakan terdeteksi, matikan setelah 10 detik tanpa gerakan.

Cara pakai:
  python3 security_light.py
"""

import rclpy                       # Library ROS2 Python — menghubungkan script ke ROS2
from rclpy.node import Node        # Class Node — membuat node ROS2 di Python
from std_msgs.msg import Bool      # Tipe pesan Bool — untuk LED ON/OFF dan deteksi gerakan
from time import time              # Library time — untuk hitung waktu timeout

class SecurityLight(Node):                               # Node ROS2 — lampu otomatis sensor gerak
    def __init__(self):
        super().__init__('security_light')               # Inisialisasi node dengan nama "security_light"
        self.pub_led = self.create_publisher(Bool, 'led', 10)  # Publisher ke topic "led"
        self.sub = self.create_subscription(             # Subscribe ke topic "gerakan"
            Bool, 'gerakan', self.cb_gerakan, 10)
        self.timer = self.create_timer(1.0, self.check_timeout)  # Timer cek timeout tiap 1 detik
        self.last_motion_time = 0                         # Waktu terakhir gerakan terdeteksi
        self.timeout = 10                                  # Lampu mati setelah 10 detik tanpa gerakan
        self.light_on = False                              # Status lampu saat ini
        print("Security light aktif. Timeout: 10 detik")

    def cb_gerakan(self, msg):                           # Callback — dipanggil saat ada data gerakan
        if msg.data:                                      # Jika gerakan terdeteksi
            self.last_motion_time = time()                # Catat waktu gerakan
            if not self.light_on:                         # Jika lampu masih mati, nyalakan
                self.light_on = True
                led_msg = Bool()
                led_msg.data = True
                self.pub_led.publish(led_msg)             # Kirim perintah ON ke LED
                print("Gerakan! Lampu ON")

    def check_timeout(self):                              # Method — cek apakah sudah waktunya matikan lampu
        if self.light_on and (time() - self.last_motion_time > self.timeout):
            self.light_on = False                          # Lewati timeout, matikan lampu
            led_msg = Bool()
            led_msg.data = False
            self.pub_led.publish(led_msg)                 # Kirim perintah OFF ke LED
            print("Timeout - Lampu OFF")

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = SecurityLight()                          # Buat instance node SecurityLight
    try:
        rclpy.spin(node)                            # Loop forever — proses callback terus
    except KeyboardInterrupt:                       # Tangani Ctrl+C
        pass
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
