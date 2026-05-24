#!/usr/bin/env python3
# ============================================================
# service_server.py — Service Server ROS2
#
# Node ini menyediakan service /add_two_ints.
# Client mengirim dua angka, server mengembalikan jumlahnya.
#
# Service berbeda dengan Topic:
# - Topic: broadcast terus-menerus (satu arah)
# - Service: request-response (dua arah, sekali panggil)
#
# Cara jalankan:
#   python3 service_server.py
#
# Lalu di terminal lain jalankan client:
#   python3 service_client.py
# ============================================================

import rclpy
from rclpy.node import Node

# AddTwoInts adalah tipe service bawaan ROS2
# Request: int64 a, int64 b
# Response: int64 sum
from example_interfaces.srv import AddTwoInts


class ServiceServerNode(Node):
    """
    Sebuah service server node.
    
    Tugasnya:
    - Menyediakan service bernama '/add_two_ints'
    - Menerima request (dua angka)
    - Mengembalikan response (jumlah kedua angka)
    """

    def __init__(self):
        super().__init__('service_server_node')

        # Buat Service Server
        # Parameter:
        #   1. Tipe service: AddTwoInts
        #   2. Nama service: 'add_two_ints'
        #   3. Callback: fungsi yang dipanggil saat ada request
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_callback
        )

        self.get_logger().info('Service server /add_two_ints siap!')

    def add_callback(self, request, response):
        """
        CALLBACK — dipanggil OTOMATIS saat ada client
        memanggil service /add_two_ints.
        
        Parameter:
        - request: berisi request.a dan request.b (int64)
        - response: harus diisi response.sum (int64)
        
        Fungsi ini HARUS mengembalikan response.
        """
        # Log request yang masuk
        self.get_logger().info(
            f'Menerima request: {request.a} + {request.b}'
        )

        # Hitung jumlah
        response.sum = request.a + request.b

        # Log response
        self.get_logger().info(
            f'Mengirim response: {response.sum}'
        )

        return response


def main():
    rclpy.init()
    node = ServiceServerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nService server dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
