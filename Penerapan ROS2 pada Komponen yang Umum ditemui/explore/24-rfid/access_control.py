#!/usr/bin/env python3
"""
access_control.py — kontrol akses berdasarkan RFID

Jika UID terdaftar → buka solenoid (unlock).
Jika tidak → tolak akses, bunyikan buzzer.

Cara pakai:
  python3 access_control.py
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
