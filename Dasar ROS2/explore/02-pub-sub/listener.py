#!/usr/bin/env python3
# ============================================================
# listener.py — Subscriber ROS2
#
# Node ini mendengarkan topic /chatter
# dan mencetak setiap pesan yang diterima.
#
# Cara jalankan:
#   python3 listener.py
#
# (Jalankan BERSAMAAN dengan talker.py di terminal lain)
# ============================================================

# ═══════════════════════════════════════════════════════════════
# PENJELASAN DATA STRUCTURE
# ═══════════════════════════════════════════════════════════════
#
# Berikut adalah data structure / objek ROS2 yang dipakai di file ini:
#
# 1. rclpy
#    - Library utama ROS2 Python. Wajib untuk semua node.
#    - rclpy.init() = inisialisasi, rclpy.spin() = loop utama.
#
# 2. Node
#    - Kelas dasar node ROS2.
#    - Setiap node punya nama unik (di sini: "listener_node").
#    - Bisa memiliki subscriber, publisher, timer, service, dll.
#
# 3. Subscription (dibuat dengan create_subscription())
#    - Objek untuk MENERIMA data dari topic ROS2.
#    - Parameter: tipe pesan, nama topic, callback, qos.
#    - Callback dipanggil OTOMATIS setiap ada data masuk.
#    - Sifat: decoupled — subscriber tidak tahu siapa publisher-nya.
#
# 4. Callback (fungsi listener_callback)
#    - Dipanggil otomatis oleh ROS2 saat ada pesan baru.
#    - Parameter: msg — object pesan berisi data.
#    - Di sini: membaca msg.data dan menampilkan ke layar.
#
# 5. std_msgs.msg.String
#    - Tipe pesan standar ROS2 untuk teks.
#    - Struktur: msg.data (string) — field tunggal berisi teks.
#
# ═══════════════════════════════════════════════════════════════

import rclpy  # (1) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (2) Kelas dasar Node untuk membuat node ROS2.
from std_msgs.msg import String  # (3) Tipe pesan standar String — sama dengan yang digunakan talker.


class ListenerNode(Node):
    # (4) Semua node ROS2 HARUS mewarisi class Node.
    """
    Sebuah subscriber node.
    
    Tugasnya:
    - Subscribe ke topic '/chatter'
    - Setiap kali ada pesan masuk, cetak isinya
    """

    def __init__(self):
        # (5) Panggil constructor parent dengan nama node UNIK.
        super().__init__('listener_node')

        # (6) MEMBUAT SUBSCRIPTION — untuk menerima data dari topic.
        # Sintaks ROS2: self.create_subscription(TipePesan, 'topic', callback, qos)
        # Parameter:
        #   1. Tipe pesan: String — harus SAMA dengan tipe yang digunakan publisher
        #   2. Nama topic: 'chatter' — harus SAMA dengan topic publisher
        #   3. Callback: fungsi yang dipanggil SETIAP ada pesan masuk
        #   4. Queue size (qos): 10 — antrean pesan sebelum diproses
        # Perbedaan dengan publisher: subscriber TIDAK mengirim data, hanya menerima.
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )

        # (7) Log bahwa node sudah siap.
        self.get_logger().info('Listener node sudah hidup!')

    def listener_callback(self, msg):
        # (8) CALLBACK SUBSCRIPTION — dipanggil OTOMATIS oleh ROS2.
        # Parameter 'msg' berisi data yang dikirim oleh publisher.
        # msg adalah objek String, sama dengan yang dibuat di talker.
        # msg.data — field string yang berisi teks pesan.
        """
        CALLBACK — dipanggil OTOMATIS setiap kali ada pesan
        masuk di topic /chatter.
        
        Parameter msg adalah objek String yang dikirim publisher.
        msg.data berisi teks yang dikirim.
        """
        self.get_logger().info(f'Menerima: "{msg.data}"')
        # (9) Pesan akan muncul SETIAP KALI talker mengirim data (setiap 1 detik).


def main():
    # (10) rclpy.init() — inisialisasi ROS2 (WAJIB dipanggil pertama).
    rclpy.init()
    # (11) Membuat instance node ListenerNode.
    node = ListenerNode()
    
    try:
        # (12) rclpy.spin(node) — loop tak terbatas, tunggu event.
        rclpy.spin(node)
    except KeyboardInterrupt:
        # (13) Tangani Ctrl+C.
        print("\nListener dihentikan.")
    finally:
        # (14) Bersihkan resource node dan shutdown ROS2.
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    # (15) Entry point: jalankan main() jika dieksekusi langsung.
    main()
