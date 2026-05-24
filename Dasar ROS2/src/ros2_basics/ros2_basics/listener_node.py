import rclpy  # (1) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (2) Kelas dasar Node untuk membuat node ROS2.
from std_msgs.msg import String  # (3) Tipe pesan standar String.


class ListenerNode(Node):
    # (4) Semua node ROS2 HARUS mewarisi class Node.
    """
    Subscriber node — menerima pesan dari topic /chatter.
    Sama seperti explore/02-pub-sub/listener.py, tapi dibungkus sebagai package.
    """

    def __init__(self):
        # (5) Panggil constructor parent dengan nama node UNIK.
        super().__init__('listener_node')
        # (6) MEMBUAT SUBSCRIPTION — self.create_subscription(Tipe, 'topic', callback, qos).
        self.subscription = self.create_subscription(
            String, 'chatter', self.listener_callback, 10
        )
        # (7) Log node siap.
        self.get_logger().info('Listener node siap!')

    def listener_callback(self, msg):
        # (8) CALLBACK SUBSCRIPTION — dipanggil OTOMATIS saat ada pesan di /chatter.
        self.get_logger().info(f'Menerima: "{msg.data}"')


def main():
    rclpy.init()  # (9) Inisialisasi ROS2 — WAJIB.
    node = ListenerNode()  # (10) Buat instance node.
    try:
        rclpy.spin(node)  # (11) Loop utama — tunggu pesan masuk.
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
