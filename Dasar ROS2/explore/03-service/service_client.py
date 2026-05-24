#!/usr/bin/env python3
# ============================================================
# service_client.py — Service Client ROS2
#
# Node ini memanggil service /add_two_ints.
# Mengirim dua angka, lalu menunggu response (jumlahnya).
#
# Cara jalankan:
#   (Pastikan service_server.py sudah jalan)
#   python3 service_client.py
# ============================================================

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

# Untuk menunggu service tersedia
import sys


class ServiceClientNode(Node):
    """
    Sebuah service client node.
    
    Tugasnya:
    - Memanggil service '/add_two_ints'
    - Mengirim request: a=5, b=3
    - Menerima response: sum=8
    """

    def __init__(self):
        super().__init__('service_client_node')

        # Buat Service Client
        # Parameter:
        #   1. Tipe service: AddTwoInts
        #   2. Nama service: 'add_two_ints'
        self.client = self.create_client(AddTwoInts, 'add_two_ints')

        # Tunggu sampai service server tersedia
        # Ini WAJIB — kalau tidak, request akan gagal
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn(
                'Service /add_two_ints belum tersedia, menunggu...'
            )

        # Buat request
        request = AddTwoInts.Request()
        request.a = 5
        request.b = 3

        self.get_logger().info(
            f'Mengirim request: {request.a} + {request.b}'
        )

        # Panggil service secara asynchronous
        # future = hasil yang akan datang (belum tentu langsung)
        self.future = self.client.call_async(request)

        # Timer untuk mengecek apakah response sudah diterima
        self.timer = self.create_timer(0.1, self.check_response)

    def check_response(self):
        """
        Mengecek apakah response dari service sudah diterima.
        Dipanggil setiap 0.1 detik oleh timer.
        """
        if self.future.done():
            try:
                # Ambil response
                response = self.future.result()
                self.get_logger().info(
                    f'Response: {response.sum}'
                )
            except Exception as e:
                self.get_logger().error(
                    f'Panggilan service gagal: {e}'
                )
            finally:
                # Hentikan node setelah selesai
                rclpy.shutdown()
                sys.exit(0)


def main():
    rclpy.init()
    node = ServiceClientNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nService client dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
