#!/usr/bin/env python3
"""
shake_detector.py — deteksi guncangan/benturan via MPU6050

Jika total percepatan > 3G, bunyikan alarm.

Cara pakai:
  python3 shake_detector.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Int32
import math

class ShakeDetector(Node):
    def __init__(self):
        # super().__init__(): buat node 'shake_detector'.
        super().__init__('shake_detector')
        # Publisher ke topic /buzzer (Int32) — nilai = frekuensi buzzer.
        self.pub = self.create_publisher(Int32, 'buzzer', 10)
        # Inisialisasi nilai accelerometer.
        self.ax = self.ay = self.az = 0.0
        # Subscribe ke 3 topic accel (dari mpu6050.ino).
        # self.cb('ax') membuat closure yang update self.ax.
        self.create_subscription(Float64, 'accel_x', self.cb('ax'), 10)
        self.create_subscription(Float64, 'accel_y', self.cb('ay'), 10)
        self.create_subscription(Float64, 'accel_z', self.cb('az'), 10)
        # Timer 0.1 detik = periksa guncangan 10x/detik.
        self.timer = self.create_timer(0.1, self.check_shake)
        self.threshold = 3.0  # G — ambang batas guncangan.
        print(f"Shake detector aktif. Threshold: {self.threshold}G")

    # cb(): factory method — menghasilkan fungsi callback yang
    # menyimpan data ke atribut sesuai nama yang diberikan.
    def cb(self, name):
        def inner(msg):
            # setattr(self, name, value): set self.nama = msg.data.
            setattr(self, name, msg.data)
        return inner

    def check_shake(self):
        # Hitung total percepatan (magnitude vektor) = sqrt(x^2+y^2+z^2).
        total_g = math.sqrt(self.ax**2 + self.ay**2 + self.az**2)
        if total_g > self.threshold:
            # get_logger().warn(): log peringatan ROS2.
            self.get_logger().warn(f'GUNCANGAN! Total: {total_g:.1f}G')
            buzzer_msg = Int32()
            buzzer_msg.data = 2500  # Frekuensi 2500 Hz.
            self.pub.publish(buzzer_msg)
        else:
            buzzer_msg = Int32()
            buzzer_msg.data = 0  # 0 = buzzer mati.
            self.pub.publish(buzzer_msg)

def main():
    rclpy.init()
    node = ShakeDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
