#!/usr/bin/env python3
# ============================================================
# talker.py — Publisher ROS2
#
# Node ini mempublikasikan pesan ke topic /chatter
# setiap 1 detik menggunakan timer.
#
# Cara jalankan:
#   python3 talker.py
#
# (Buka terminal terpisah untuk subscriber)
# ============================================================

# ═══════════════════════════════════════════════════════════════
# PENJELASAN DATA STRUCTURE
# ═══════════════════════════════════════════════════════════════
#
# Berikut adalah data structure / objek ROS2 yang dipakai di file ini:
#
# 1. rclpy
#    - Library utama ROS2 Python. Wajib untuk semua program.
#    - rclpy.init() = inisialisasi koneksi ke ROS2.
#    - rclpy.spin() = loop utama yang menjaga node tetap aktif.
#
# 2. Node
#    - Kelas dasar untuk membuat node ROS2.
#    - Seperti "program" dalam sistem ROS2 — punya nama unik.
#    - Bisa memiliki publisher, subscriber, service, timer, dll.
#
# 3. Publisher (dibuat dengan create_publisher())
#    - Objek untuk MENGIRIM data ke topic ROS2.
#    - Parameter: tipe pesan, nama topic, queue size.
#    - Method: publish(msg) — kirim pesan ke semua subscriber.
#    - Sifat: decoupled — publisher tidak tahu siapa subscriber-nya.
#
# 4. std_msgs.msg.String
#    - Tipe pesan standar ROS2 untuk teks.
#    - Struktur: msg.data (bertipe string).
#    - ROS2 punya banyak tipe bawaan: Int32, Float32, Bool, Header, dll.
#
# 5. Timer (create_timer())
#    - Memanggil callback secara periodik.
#    - Parameter: interval_detik, callback_function.
#    - Digunakan di sini untuk publish data setiap 1 detik.
#
# ═══════════════════════════════════════════════════════════════

import rclpy  # (1) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (2) Kelas dasar Node untuk membuat node ROS2.

# (3) std_msgs.msg.String — tipe pesan standar ROS2 untuk teks.
# Berisi satu field: msg.data (bertipe string).
# ROS2 menyediakan banyak tipe bawaan: String, Int32, Float32, Bool, dll.
from std_msgs.msg import String


class TalkerNode(Node):
    # (4) Semua node ROS2 HARUS mewarisi class Node.
    """
    Sebuah publisher node.
    
    Tugasnya:
    - Membuat topic bernama '/chatter'
    - Mengirim pesan String ke topic itu setiap 1 detik
    """

    def __init__(self):
        # (5) Panggil constructor parent class dengan nama node UNIK.
        # Nama node: 'talker_node' — akan muncul di 'ros2 node list'.
        super().__init__('talker_node')

        # (6) MEMBUAT PUBLISHER — untuk mengirim data ke topic.
        # Sintaks ROS2: self.create_publisher(TipePesan, 'nama_topic', qos)
        # Parameter:
        #   1. Tipe pesan: String (dari std_msgs.msg)
        #   2. Nama topic: 'chatter' (subscriber harus subscribe ke topic SAMA)
        #   3. Queue size (qos): 10 — maksimum pesan di antre sebelum dibuang
        # Publisher ini akan mengirim pesan String ke topic '/chatter'.
        self.publisher = self.create_publisher(String, 'chatter', 10)

        # (7) Timer periodik — trigger callback setiap 1 detik.
        # Sintaks: self.create_timer(interval_detik, callback)
        # interval: 1.0 detik. callback: self.timer_callback.
        self.timer = self.create_timer(1.0, self.timer_callback)

        # (8) Variabel instance untuk memberi nomor pada setiap pesan.
        self.count = 0

        # (9) Log bahwa node sudah siap berjalan.
        self.get_logger().info('Talker node sudah hidup!')

    def timer_callback(self):
        # (10) CALLBACK TIMER — dipanggil OTOMATIS setiap 1 detik.
        """
        Dipanggil setiap 1 detik oleh timer.
        Membuat pesan String dan mempublikasikannya.
        """
        # (11) Membuat objek pesan String (kosong).
        msg = String()
        # (12) Mengisi field 'data' dengan teks yang akan dikirim.
        msg.data = f'Halo ROS2! Pesan ke-{self.count}'

        # (13) PUBLISH — mengirim pesan ke topic /chatter.
        # Sintaks: self.publisher.publish(isi_pesan)
        # Semua subscriber yang subscribe ke /chatter akan menerima pesan ini.
        self.publisher.publish(msg)

        # (14) Log konfirmasi bahwa pesan telah dikirim.
        self.get_logger().info(f'Mengirim: "{msg.data}"')

        # (15) Increment counter untuk pesan berikutnya.
        self.count += 1


def main():
    # (16) rclpy.init() — inisialisasi ROS2 (WAJIB).
    rclpy.init()
    # (17) Membuat instance node TalkerNode.
    node = TalkerNode()
    
    try:
        # (18) rclpy.spin(node) — loop utama ROS2, tunggu event.
        rclpy.spin(node)
    except KeyboardInterrupt:
        # (19) Tangani Ctrl+C.
        print("\nTalker dihentikan.")
    finally:
        # (20) Bersihkan node dan shutdown ROS2.
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    # (21) Entry point: jalankan main() jika file dieksekusi langsung.
    main()
