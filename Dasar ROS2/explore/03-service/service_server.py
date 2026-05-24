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

import rclpy  # (1) Library utama ROS2 Python. Wajib untuk semua program.
from rclpy.node import Node  # (2) Kelas dasar Node untuk membuat node ROS2.

# (3) AddTwoInts — tipe service bawaan ROS2 dari package example_interfaces.
# Struktur AddTwoInts:
#   Request:  int64 a, int64 b    (input: dua angka)
#   Response: int64 sum           (output: jumlah kedua angka)
# Service selalu memiliki Request dan Response.
from example_interfaces.srv import AddTwoInts


class ServiceServerNode(Node):
    # (4) Semua node ROS2 HARUS mewarisi class Node.
    """
    Sebuah service server node.
    
    Tugasnya:
    - Menyediakan service bernama '/add_two_ints'
    - Menerima request (dua angka)
    - Mengembalikan response (jumlah kedua angka)
    """

    def __init__(self):
        # (5) Panggil constructor parent dengan nama node UNIK.
        super().__init__('service_server_node')

        # (6) MEMBUAT SERVICE SERVER — menyediakan layanan request-response.
        # Sintaks ROS2: self.create_service(TipeService, 'nama_service', callback)
        # Parameter:
        #   1. Tipe service: AddTwoInts — menentukan format request & response
        #   2. Nama service: 'add_two_ints' — client akan memanggil nama INI
        #   3. Callback: fungsi yang dipanggil SETIAP ada request dari client
        # Perbedaan dengan Publisher:
        #   Publisher → broadcast (satu arah, terus-menerus)
        #   Service → request-response (dua arah, hanya saat dipanggil)
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_callback
        )

        # (7) Log bahwa server sudah siap melayani request.
        self.get_logger().info('Service server /add_two_ints siap!')

    def add_callback(self, request, response):
        # (8) CALLBACK SERVICE — dipanggil OTOMATIS saat client memanggil service.
        # Parameter callback service SELALU: (request, response).
        #   - request: objek berisi data yang dikirim client
        #   - response: objek yang harus kita isi untuk dikembalikan ke client
        # Fungsi ini HARUS mengembalikan (return) response.
        """
        CALLBACK — dipanggil OTOMATIS saat ada client
        memanggil service /add_two_ints.
        
        Parameter:
        - request: berisi request.a dan request.b (int64)
        - response: harus diisi response.sum (int64)
        
        Fungsi ini HARUS mengembalikan response.
        """
        # (9) Log request yang masuk dari client.
        # request.a dan request.b adalah field dari AddTwoInts.Request.
        self.get_logger().info(
            f'Menerima request: {request.a} + {request.b}'
        )

        # (10) Proses: jumlahkan kedua angka dari request.
        # response.sum adalah field dari AddTwoInts.Response.
        response.sum = request.a + request.b

        # (11) Log response yang akan dikirim balik ke client.
        self.get_logger().info(
            f'Mengirim response: {response.sum}'
        )

        # (12) WAJIB: kembalikan response ke client.
        return response


def main():
    # (13) rclpy.init() — inisialisasi ROS2 (WAJIB).
    rclpy.init()
    # (14) Membuat instance node ServiceServerNode.
    node = ServiceServerNode()
    
    try:
        # (15) rclpy.spin(node) — loop utama, tunggu request dari client.
        rclpy.spin(node)
    except KeyboardInterrupt:
        # (16) Tangani Ctrl+C.
        print("\nService server dihentikan.")
    finally:
        # (17) Bersihkan node dan shutdown ROS2.
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    # (18) Entry point: jalankan main() jika dieksekusi langsung.
    main()
