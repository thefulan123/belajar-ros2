#!/usr/bin/env python3
import rclpy  # (1) Library utama ROS2 Python.
from rclpy.node import Node  # (2) Kelas dasar Node.
from example_interfaces.srv import AddTwoInts  # (3) Tipe service AddTwoInts (request: a,b; response: sum).


class ServiceServerNode(Node):
    # (4) Semua node ROS2 HARUS mewarisi class Node.
    def __init__(self):
        # (5) Panggil constructor parent dengan nama node UNIK.
        super().__init__('service_server_node')
        # (6) MEMBUAT SERVICE SERVER — self.create_service(Tipe, 'nama', callback).
        self.srv = self.create_service(
            AddTwoInts, 'add_two_ints', self.add_callback
        )
        # (7) Log server siap.
        self.get_logger().info('Service server /add_two_ints siap!')

    def add_callback(self, request, response):
        # (8) CALLBACK SERVICE — dipanggil OTOMATIS saat ada request.
        # request: objek dengan field a, b. response: objek dengan field sum.
        self.get_logger().info(f'Menerima: {request.a} + {request.b}')
        response.sum = request.a + request.b  # (9) Jumlahkan, isi response.
        self.get_logger().info(f'Mengirim: {response.sum}')
        return response  # (10) WAJIB: kembalikan response ke client.


def main():
    rclpy.init()  # (11) Inisialisasi ROS2 — WAJIB.
    node = ServiceServerNode()
    try:
        rclpy.spin(node)  # (12) Loop utama — tunggu request.
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
