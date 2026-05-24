#!/usr/bin/env python3
"""
servo_sweep.py — gerakkan servo maju-mundur (sweep)

Cara pakai:
  python3 servo_sweep.py
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

# rclpy: library client ROS2 untuk Python.
import rclpy
# Node: kelas dasar untuk membuat node ROS2.
from rclpy.node import Node
# Int32: tipe pesan integer 32-bit.
from std_msgs.msg import Int32
import time

class ServoSweep(Node):
    def __init__(self):
        # super().__init__(): panggil konstruktor Node dengan nama node.
        super().__init__('servo_sweep')
        # create_publisher(Int32, 'servo', 10): buat publisher untuk topic /servo.
        # 10 = queue size (maks jumlah pesan yang diantre).
        self.pub = self.create_publisher(Int32, 'servo', 10)

    def run(self):
        print("Servo sweep... Tekan Ctrl+C untuk stop")
        try:
            # rclpy.ok(): True selama ROS2 belum di-shutdown.
            while rclpy.ok():
                # Sweep maju: 0° → 180°, step 10°.
                for sudut in range(0, 181, 10):
                    msg = Int32()
                    msg.data = sudut
                    # publish(): kirim pesan ke topic /servo.
                    self.pub.publish(msg)
                    # get_logger().info(): logging ROS2 (muncul di console).
                    self.get_logger().info(f'Servo: {sudut}°')
                    time.sleep(0.3)
                    # spin_once(): proses callback (penting agar timer/sub berfungsi).
                    rclpy.spin_once(self, timeout_sec=0)
                # Sweep mundur: 180° → 0°, step -10°.
                for sudut in range(180, -1, -10):
                    msg = Int32()
                    msg.data = sudut
                    self.pub.publish(msg)
                    self.get_logger().info(f'Servo: {sudut}°')
                    time.sleep(0.3)
                    rclpy.spin_once(self, timeout_sec=0)
        except KeyboardInterrupt:
            pass

def main():
    # rclpy.init(): inisialisasi sistem ROS2 (wajib sebelum apapun).
    rclpy.init()
    # Buat instance node.
    node = ServoSweep()
    try:
        node.run()
    finally:
        # destroy_node(): bersihkan resource node.
        node.destroy_node()
        # rclpy.shutdown(): matikan sistem ROS2.
        rclpy.shutdown()

if __name__ == '__main__':
    main()
