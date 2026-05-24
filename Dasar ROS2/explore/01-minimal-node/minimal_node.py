#!/usr/bin/env python3
# ============================================================
# minimal_node.py — Node ROS2 paling sederhana
#
# Apa yang dipelajari:
# - Cara membuat node ROS2
# - Cara menggunakan timer dan callback
# - Cara menjalankan node dengan rclpy.spin()
#
# Cara jalankan:
#   python3 minimal_node.py
#
# (Tidak perlu colcon build — langsung jalan)
# ============================================================

# ═══════════════════════════════════════════════════════════════
# PENJELASAN DATA STRUCTURE
# ═══════════════════════════════════════════════════════════════
#
# Berikut adalah data structure / objek ROS2 yang dipakai di file ini:
#
# 1. rclpy
#    - Library utama ROS2 untuk Bahasa Python.
#    - Wajib dipanggil di setiap program ROS2 Python.
#    - Fungsi utama: rclpy.init() untuk inisialisasi, rclpy.spin() untuk loop.
#
# 2. Node (dari rclpy.node)
#    - Kelas dasar untuk membuat node ROS2.
#    - Semua node HARUS mewarisi (inherit) class ini.
#    - Method penting: create_timer(), get_logger(), destroy_node().
#
# 3. Timer
#    - Bukan class terpisah, tapi objek hasil create_timer(interval, callback).
#    - Memanggil fungsi callback secara periodik setiap interval detik.
#    - Berguna untuk tugas berulang: publish data, baca sensor, dll.
#
# 4. Callback
#    - Fungsi yang dipanggil OTOMATIS oleh ROS2 saat event terjadi.
#    - Contoh: timer callback, subscriber callback, service callback.
#    - Tidak dipanggil langsung oleh kode kita, tapi oleh rclpy.spin().
#
# 5. rclpy.spin(node)
#    - Fungsi utama yang menjaga program tetap berjalan.
#    - Mendengarkan event (timer, topic, service) dan memanggil callback.
#    - Tanpa spin(), program akan selesai langsung setelah inisialisasi.
#
# ═══════════════════════════════════════════════════════════════

import rclpy  # (1) Import library utama ROS2 untuk Python. WAJIB untuk semua program ROS2.
from rclpy.node import Node  # (2) Import class Node — kelas dasar untuk membuat node ROS2.


class MinimalNode(Node):
    # (3) Semua node ROS2 harus mewarisi (inherit) dari class Node.
    """
    Sebuah node ROS2 sederhana.
    
    Node ini:
    - Punya nama: 'minimal_node'
    - Punya timer yang memanggil callback tiap 1 detik
    - Mencetak pesan setiap kali callback dipanggil
    """

    def __init__(self):
        # (4) Constructor dipanggil saat objek node dibuat.
        # Panggil constructor Node dengan nama 'minimal_node'
        # Nama ini yang akan muncul di ros2 node list
        # Sintaks: super().__init__('nama_node') — nama_node harus UNIK.
        super().__init__('minimal_node')

        # (5) Timer periodik — memanggil callback setiap N detik.
        # Sintaks: self.create_timer(interval_detik, callback_function)
        # interval_detik: float, misal 1.0 = 1 detik, 0.5 = 500 ms.
        # callback_function: fungsi yang dipanggil OTOMATIS oleh ROS2.
        self.timer = self.create_timer(1.0, self.callback_timer)

        # (6) Logging ROS2 — mencetak pesan ke terminal dengan format bawaan ROS2.
        # Sintaks: self.get_logger().info('pesan')
        # self.get_logger() mengembalikan objek logger milik node ini.
        # info(), warn(), error() untuk level log berbeda.
        self.get_logger().info('Node minimal_node sudah hidup!')

    def callback_timer(self):
        # (7) CALLBACK — fungsi yang dipanggil OTOMATIS oleh timer.
        # Kita TIDAK perlu memanggil fungsi ini secara langsung.
        # ROS2 memanggilnya setiap interval yang ditentukan.
        """
        Fungsi ini dipanggil otomatis oleh timer setiap 1 detik.
        Ini adalah CALLBACK — fungsi yang dipanggil oleh sistem,
        bukan oleh kode kita secara langsung.
        """
        self.get_logger().info('Halo dari node ROS2!')
        # (8) Setiap kali timer aktif, pesan ini muncul di terminal.


def main():
    # (9) Fungsi utama — entry point program ROS2.
    """
    Fungsi utama — entry point program.
    
    Alur:
    1. rclpy.init() — inisialisasi ROS2
    2. Buat node
    3. rclpy.spin(node) — jaga program tetap hidup
    4. (Ctrl+C untuk berhenti)
    """

    # (10) rclpy.init() — WAJIB dipanggil PERTAMA KALI.
    # Fungsi ini menginisialisasi komunikasi ROS2 (DDS, middleware).
    # Tanpa ini, node ROS2 tidak bisa berkomunikasi.
    # Hanya dipanggil SEKALI dalam satu proses.
    rclpy.init()

    # (11) Membuat instance node — object dari class MinimalNode.
    # Constructor(__init__) akan dijalankan secara otomatis.
    node = MinimalNode()

    # (12) rclpy.spin(node) — loop tak terbatas (infinite loop).
    # spin() mendengarkan event (timer, topic, service, action).
    # Setiap event memicu callback yang sesuai.
    # Tanpa spin(), program akan langsung selesai.
    # spin() hanya keluar saat program dihentikan (Ctrl+C).
    print("Node berjalan. Tekan Ctrl+C untuk berhenti.")
    
    try:
        rclpy.spin(node)  # (13) Loop utama ROS2 — blokir di sini sampai dihentikan.
    except KeyboardInterrupt:
        # (14) Menangkap sinyal Ctrl+C dari pengguna.
        print("\nNode dihentikan oleh pengguna.")
    finally:
        # (15) Membersihkan resource node — membebaskan memori.
        node.destroy_node()
        # (16) rclpy.shutdown() — membersihkan koneksi ROS2.
        # Harus dipanggil saat program selesai.
        rclpy.shutdown()


if __name__ == '__main__':
    # (17) Idiom Python: jalankan main() jika file ini dieksekusi langsung.
    # Jika file di-import, main() TIDAK dijalankan otomatis.
    main()
