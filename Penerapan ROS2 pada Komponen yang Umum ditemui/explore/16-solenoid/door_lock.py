#!/usr/bin/env python3
"""
door_lock.py — smart door lock

Buka kunci selama 5 detik, lalu kunci lagi.
Gunakan push button (topic /button) untuk trigger unlock.

Cara pakai:
  python3 door_lock.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from time import time

class DoorLock(Node):
    def __init__(self):
        # super().__init__(): inisialisasi node dengan nama 'door_lock'.
        super().__init__('door_lock')
        # Publisher ke topic /solenoid (Bool) untuk kontrol kunci.
        self.pub = self.create_publisher(Bool, 'solenoid', 10)
        # Subscriber ke topic /button — terima sinyal dari tombol.
        self.sub = self.create_subscription(
            Bool, 'button', self.cb_button, 10)
        # Timer periodik 0.5 detik untuk cek apakah perlu mengunci kembali.
        self.timer = self.create_timer(0.5, self.check_timer)
        self.unlock_until = 0       # Timestamp kapan harus dikunci lagi.
        self.locked = True          # Status kunci: True = terkunci.
        self.unlock_duration = 5    # detik — lama terbuka.
        print("Smart door lock siap. Tekan tombol untuk unlock 5 detik.")
        # Pastikan terkunci saat start.
        self.pub.publish(Bool(data=False))

    def cb_button(self, msg):
        # msg.data = True menandakan tombol ditekan.
        if msg.data:  # Tombol ditekan
            # Catat waktu kapan harus mengunci kembali.
            self.unlock_until = time() + self.unlock_duration
            if self.locked:
                self.locked = False
                # Kirim True → solenoid ON (kunci terbuka).
                self.pub.publish(Bool(data=True))
                print("🔓 Door UNLOCKED (5 detik)")

    def check_timer(self):
        # Timer: jika sedang terbuka dan waktu sudah habis → kunci lagi.
        if not self.locked and time() > self.unlock_until:
            self.locked = True
            # Kirim False → solenoid OFF (kunci tertutup).
            self.pub.publish(Bool(data=False))
            print("🔒 Door LOCKED kembali")

def main():
    # rclpy.init(): wajib — inisialisasi komunikasi ROS2.
    rclpy.init()
    node = DoorLock()
    try:
        # rclpy.spin(node): loop utama — proses callback terus-menerus.
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
