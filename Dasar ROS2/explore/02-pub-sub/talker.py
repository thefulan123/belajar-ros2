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

import rclpy
from rclpy.node import Node

# std_msgs.msg.String adalah tipe pesan standar ROS2
# Berisi satu field: data (string)
from std_msgs.msg import String


class TalkerNode(Node):
    """
    Sebuah publisher node.
    
    Tugasnya:
    - Membuat topic bernama '/chatter'
    - Mengirim pesan String ke topic itu setiap 1 detik
    """

    def __init__(self):
        super().__init__('talker_node')

        # Buat Publisher
        # Parameter:
        #   1. Tipe pesan: String
        #   2. Nama topic: 'chatter'
        #   3. Queue size: 10 (pesan yang diantre jika subscriber lambat)
        self.publisher = self.create_publisher(String, 'chatter', 10)

        # Timer — kirim pesan setiap 1 detik
        self.timer = self.create_timer(1.0, self.timer_callback)

        # Counter untuk variasi pesan
        self.count = 0

        self.get_logger().info('Talker node sudah hidup!')

    def timer_callback(self):
        """
        Dipanggil setiap 1 detik oleh timer.
        Membuat pesan String dan mempublikasikannya.
        """
        # Buat pesan
        msg = String()
        msg.data = f'Halo ROS2! Pesan ke-{self.count}'

        # Publikasikan pesan ke topic /chatter
        self.publisher.publish(msg)

        # Log untuk konfirmasi
        self.get_logger().info(f'Mengirim: "{msg.data}"')

        self.count += 1


def main():
    rclpy.init()
    node = TalkerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nTalker dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
