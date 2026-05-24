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

import rclpy
from rclpy.node import Node


class MinimalNode(Node):
    """
    Sebuah node ROS2 sederhana.
    
    Node ini:
    - Punya nama: 'minimal_node'
    - Punya timer yang memanggil callback tiap 1 detik
    - Mencetak pesan setiap kali callback dipanggil
    """

    def __init__(self):
        # Panggil constructor Node dengan nama 'minimal_node'
        # Nama ini yang akan muncul di ros2 node list
        super().__init__('minimal_node')

        # Timer akan memanggil self.callback_timer SETIAP 1 detik
        # Parameter 1: interval dalam detik (float)
        # Parameter 2: fungsi callback yang dipanggil
        self.timer = self.create_timer(1.0, self.callback_timer)

        # Logger untuk mencetak pesan
        self.get_logger().info('Node minimal_node sudah hidup!')

    def callback_timer(self):
        """
        Fungsi ini dipanggil otomatis oleh timer setiap 1 detik.
        Ini adalah CALLBACK — fungsi yang dipanggil oleh sistem,
        bukan oleh kode kita secara langsung.
        """
        self.get_logger().info('Halo dari node ROS2!')


def main():
    """
    Fungsi utama — entry point program.
    
    Alur:
    1. rclpy.init() — inisialisasi ROS2
    2. Buat node
    3. rclpy.spin(node) — jaga program tetap hidup
    4. (Ctrl+C untuk berhenti)
    """

    # 1. Inisialisasi ROS2
    # Wajib dipanggil SEBELUM membuat node
    rclpy.init()

    # 2. Buat node
    node = MinimalNode()

    # 3. rclpy.spin() menjaga program tetap hidup
    # Tanpa ini, program akan langsung selesai.
    # spin() mendengarkan event (timer, topic, service)
    # dan memanggil callback yang sesuai.
    print("Node berjalan. Tekan Ctrl+C untuk berhenti.")
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Tangani Ctrl+C
        print("\nNode dihentikan oleh pengguna.")
    finally:
        # Bersihkan resource
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
