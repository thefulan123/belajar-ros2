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

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ListenerNode(Node):
    """
    Sebuah subscriber node.
    
    Tugasnya:
    - Subscribe ke topic '/chatter'
    - Setiap kali ada pesan masuk, cetak isinya
    """

    def __init__(self):
        super().__init__('listener_node')

        # Buat Subscription
        # Parameter:
        #   1. Tipe pesan: String
        #   2. Nama topic: 'chatter'
        #   3. Callback: fungsi yang dipanggil saat ada pesan masuk
        #   4. Queue size: 10
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )

        self.get_logger().info('Listener node sudah hidup!')

    def listener_callback(self, msg):
        """
        CALLBACK — dipanggil OTOMATIS setiap kali ada pesan
        masuk di topic /chatter.
        
        Parameter msg adalah objek String yang dikirim publisher.
        msg.data berisi teks yang dikirim.
        """
        self.get_logger().info(f'Menerima: "{msg.data}"')


def main():
    rclpy.init()
    node = ListenerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nListener dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
