#!/usr/bin/env python3
"""
shake_detector.py — deteksi guncangan/benturan via MPU6050

Jika total percepatan > 3G, bunyikan alarm.

Cara pakai:
  python3 shake_detector.py
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
