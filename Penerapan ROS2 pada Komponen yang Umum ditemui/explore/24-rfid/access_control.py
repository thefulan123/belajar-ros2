#!/usr/bin/env python3
"""
access_control.py — kontrol akses berdasarkan RFID

Jika UID terdaftar → buka solenoid (unlock).
Jika tidak → tolak akses, bunyikan buzzer.

Cara pakai:
  python3 access_control.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool, Int32

class AccessControl(Node):
    def __init__(self):
        # super().__init__(): buat node 'access_control'.
        super().__init__('access_control')
        # Publisher ke topic /solenoid (Bool) untuk kunci pintu.
        self.pub_solenoid = self.create_publisher(Bool, 'solenoid', 10)
        # Publisher ke topic /buzzer (Int32) untuk alarm.
        self.pub_buzzer = self.create_publisher(Int32, 'buzzer', 10)
        # Subscribe ke topic /rfid (String) — dari rfid.ino.
        self.sub = self.create_subscription(
            String, 'rfid', self.cb_rfid, 10)

        # Daftar UID yang diizinkan masuk.
        # Ganti dengan UID kartu/tag RFID Anda.
        self.authorized_uids = {
            "A1:B2:C3:D4",  # Ganti dengan UID kartu Anda
            "11:22:33:44",  # Ganti dengan UID tag Anda
        }
        print(f"Access control aktif. {len(self.authorized_uids)} UID terdaftar.")

    def cb_rfid(self, msg):
        uid = msg.data
        if uid in self.authorized_uids:
            self.get_logger().info(f'✅ Akses DITERIMA: {uid}')
            # Buka solenoid 3 detik.
            self.pub_solenoid.publish(Bool(data=True))
            # create_timer(3.0, ...): timer satu-kali setelah 3 detik.
            self.create_timer(3.0, self.lock_back)
        else:
            self.get_logger().warn(f'❌ Akses DITOLAK: {uid}')
            # Bunyikan buzzer alarm (500 Hz).
            self.pub_buzzer.publish(Int32(data=500))
            self.create_timer(1.0, self.buzzer_off)

    def lock_back(self):
        # Kunci kembali: kirim False ke solenoid.
        self.pub_solenoid.publish(Bool(data=False))

    def buzzer_off(self):
        # Matikan buzzer: kirim 0.
        self.pub_buzzer.publish(Int32(data=0))

def main():
    rclpy.init()
    node = AccessControl()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
