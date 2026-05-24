#!/usr/bin/env python3
"""
password_lock.py — kunci pintu dengan password keypad

Masukkan password 4 digit + "#" untuk unlock.

Cara pakai:
  python3 password_lock.py
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
