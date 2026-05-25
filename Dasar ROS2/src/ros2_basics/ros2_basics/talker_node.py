#!/usr/bin/env python3
import rclpy  # (1) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (2) Kelas dasar Node untuk membuat node ROS2.
from std_msgs.msg import String  # (3) Tipe pesan standar String untuk komunikasi topic.


class TalkerNode(Node):
    # (4) Semua node ROS2 HARUS mewarisi class Node.
    """
    Publisher node — mengirim pesan ke topic /chatter setiap 1 detik.
    Sama seperti explore/02-pub-sub/talker.py, tapi dibungkus sebagai package.
    """

    def __init__(self):
        # (5) Panggil constructor parent dengan nama node UNIK.
        super().__init__('talker_node')
        # (6) MEMBUAT PUBLISHER — self.create_publisher(Tipe, 'topic', qos).
        self.publisher = self.create_publisher(String, 'chatter', 10)
        # (7) Timer periodik — self.create_timer(interval, callback).
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0  # (8) Counter untuk variasi pesan.
        # (9) Log node siap — self.get_logger().info().
        self.get_logger().info('Talker node siap!')

    def timer_callback(self):
        # (10) CALLBACK TIMER — dipanggil OTOMATIS setiap 1 detik.
        msg = String()  # (11) Buat objek pesan String kosong.
        msg.data = f'Halo ROS2! Pesan ke-{self.count}'  # (12) Isi field data.
        self.publisher.publish(msg)  # (13) PUBLISH — kirim ke topic /chatter.
        # (14) Log konfirmasi pengiriman.
        self.get_logger().info(f'Mengirim: "{msg.data}"')
        self.count += 1  # (15) Increment counter.


def main():
    rclpy.init()  # (16) Inisialisasi ROS2 — WAJIB dipanggil pertama.
    node = TalkerNode()  # (17) Buat instance node.
    try:
        rclpy.spin(node)  # (18) Loop utama ROS2 — tunggu event.
    except KeyboardInterrupt:
        pass  # (19) Ctrl+C: tidak perlu pesan error.
    finally:
        node.destroy_node()  # (20) Bersihkan node.
        rclpy.shutdown()  # (21) Hentikan ROS2.


if __name__ == '__main__':
    main()  # (22) Entry point: jalankan main().
