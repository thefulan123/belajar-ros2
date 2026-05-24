#!/usr/bin/env python3
"""
button_publisher.py — PC-side publisher button (simulasi)

Kegunaan:
- Untuk testing subscriber LED (explore/01) tanpa hardware button
- Publikasikan false/true untuk LED

Cara pakai:
  python3 button_publisher.py
  # Ketik "1" untuk nyalakan LED, "0" untuk matikan
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

import rclpy                       # Library ROS2 Python — menghubungkan script ke ROS2
from rclpy.node import Node        # Class Node — membuat node ROS2 di Python
from std_msgs.msg import Bool      # Tipe pesan Bool (true/false) — standar ROS2

class ButtonPublisher(Node):                        # Node ROS2 untuk simulasi button dari PC
    def __init__(self):
        super().__init__('button_publisher')        # Inisialisasi node dengan nama "button_publisher"
        self.pub = self.create_publisher(Bool, 'button', 10)  # Buat publisher di topic "button", QoS 10

    def run(self):                                  # Method utama — loop input dari keyboard
        print("Ketik '1' untuk true, '0' untuk false, 'q' untuk quit:")
        while rclpy.ok():                           # Loop selama ROS2 masih berjalan
            rclpy.spin_once(self, timeout_sec=0.1)  # Proses callback ROS2 (timeout 0.1 detik)
            cmd = input()                           # Baca input dari keyboard
            if cmd == 'q':
                break                               # Keluar jika user ketik 'q'
            msg = Bool()                            # Buat objek pesan Bool
            msg.data = (cmd == '1')                 # '1' → True, lainnya → False
            self.pub.publish(msg)                   # Kirim pesan ke topic "button"
            print(f"Published: {msg.data}")

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = ButtonPublisher()                        # Buat instance node ButtonPublisher
    try:
        node.run()                                  # Jalankan loop utama
    except KeyboardInterrupt:                       # Tangani Ctrl+C
        pass
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
