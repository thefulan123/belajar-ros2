#!/usr/bin/env python3
"""
password_lock.py — kunci pintu dengan password keypad

Masukkan password 4 digit + "#" untuk unlock.

Cara pakai:
  python3 password_lock.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool, Int32

class PasswordLock(Node):
    def __init__(self):
        # super().__init__(): buat node 'password_lock'.
        super().__init__('password_lock')
        # Publisher ke topic /solenoid (Bool) untuk kunci pintu.
        self.pub_solenoid = self.create_publisher(Bool, 'solenoid', 10)
        # Publisher ke topic /buzzer (Int32) untuk alarm sukses/gagal.
        self.pub_buzzer = self.create_publisher(Int32, 'buzzer', 10)
        # Subscribe ke topic /keypad (String) — dari keypad.ino.
        self.sub = self.create_subscription(
            String, 'keypad', self.cb_key, 10)
        self.pin = ""           # Buffer PIN yang sedang dimasukkan.
        self.password = "1234"  # GANTI dengan password Anda.
        self.max_len = 4        # Panjang password.
        print(f"Password lock aktif. Masukkan {self.max_len} digit + #")
        # Pastikan terkunci saat startup.
        self.pub_solenoid.publish(Bool(data=False))

    def cb_key(self, msg):
        key = msg.data

        # Jika '#' → konfirmasi password.
        if key == '#':
            # Cek password.
            if self.pin == self.password:
                self.get_logger().info('✅ Password benar! Buka kunci.')
                # Buka solenoid.
                self.pub_solenoid.publish(Bool(data=True))
                # Bunyi buzzer 2000 Hz (sukses).
                self.pub_buzzer.publish(Int32(data=2000))
                # Timer satu-kali: matikan buzzer setelah 0.2 detik.
                self.create_timer(0.2, self.buzzer_off)
                # Timer satu-kali: kunci kembali setelah 5 detik.
                self.create_timer(5.0, self.lock_back)
            else:
                self.get_logger().warn(f'❌ Password salah!')
                # Bunyi buzzer 100 Hz (gagal).
                self.pub_buzzer.publish(Int32(data=100))
                self.create_timer(0.5, self.buzzer_off)
            self.pin = ""  # Reset buffer setelah selesai.
        elif key == '*':
            # '*' → reset/hapus PIN yang sudah diketik.
            self.pin = ""
            print("PIN direset")
        else:
            # Tombol angka: tambahkan ke buffer PIN.
            if len(self.pin) < self.max_len:
                self.pin += key
                stars = '*' * len(self.pin)
                print(f"PIN: {stars}")  # Tampilkan asterisk (keamanan).

    def lock_back(self):
        # Kirim False → solenoid mati → pintu terkunci.
        self.pub_solenoid.publish(Bool(data=False))
        print("Terkunci kembali")

    def buzzer_off(self):
        # Kirim 0 → buzzer mati.
        self.pub_buzzer.publish(Int32(data=0))

def main():
    # rclpy.init(): inisialisasi sistem ROS2.
    rclpy.init()
    node = PasswordLock()
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
